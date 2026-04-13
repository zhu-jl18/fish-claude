import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, readFileSync, realpathSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

type Mode = "apply" | "check" | "reverse" | "check-reverse" | "status";
type PatchState = "can-apply" | "already-applied" | "needs-rebase";

type GitApplyResult = {
	ok: boolean;
	status: number | null;
	stdout: string;
	stderr: string;
};

const EXIT_OK = 0;
const EXIT_GENERIC_FAILURE = 1;
const EXIT_NEEDS_REBASE = 2;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const patchPath = path.join(__dirname, "patch.diff");

function parseMode(argv: string[]): Mode {
	if (argv.includes("--status")) return "status";
	if (argv.includes("--check-reverse")) return "check-reverse";
	if (argv.includes("--reverse")) return "reverse";
	if (argv.includes("--check")) return "check";
	return "apply";
}

function resolveOmpBinary(): string {
	const override = process.env.OMP_PATCH_OMP_BIN?.trim();
	if (override) {
		return realpathSync(override);
	}
	const whichOutput = execFileSync("which", ["omp"], { encoding: "utf8" }).trim();
	if (!whichOutput) {
		throw new Error("Could not find `omp` in PATH. Set OMP_PATCH_OMP_BIN to override.");
	}
	return realpathSync(whichOutput);
}

function isOmpPackageRoot(dir: string): boolean {
	const pkgJsonPath = path.join(dir, "package.json");
	if (!existsSync(pkgJsonPath)) return false;
	try {
		const pkg = JSON.parse(readFileSync(pkgJsonPath, "utf8")) as { name?: string };
		return pkg.name === "@oh-my-pi/pi-coding-agent";
	} catch {
		return false;
	}
}

function findOmpPackageRoot(entryPath: string): string {
	const override = process.env.OMP_PATCH_PACKAGE_ROOT?.trim();
	if (override) {
		return realpathSync(override);
	}

	const candidateRoots = [
		path.resolve(path.dirname(entryPath), "..", "lib", "node_modules", "@oh-my-pi", "pi-coding-agent"),
		path.resolve(path.dirname(entryPath), "..", "..", "lib", "node_modules", "@oh-my-pi", "pi-coding-agent"),
	];
	for (const candidate of candidateRoots) {
		if (isOmpPackageRoot(candidate)) return candidate;
	}

	try {
		const npmRoot = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
		const candidate = path.join(npmRoot, "@oh-my-pi", "pi-coding-agent");
		if (isOmpPackageRoot(candidate)) return candidate;
	} catch {}

	let dir = path.dirname(entryPath);
	while (true) {
		if (isOmpPackageRoot(dir)) return dir;
		const parent = path.dirname(dir);
		if (parent === dir) break;
		dir = parent;
	}
	throw new Error(
		`Could not locate @oh-my-pi/pi-coding-agent package root from ${entryPath}. Set OMP_PATCH_PACKAGE_ROOT to override.`,
	);
}

function gitApplyArgs(packageRoot: string, mode: Exclude<Mode, "status">): string[] {
	const args = ["apply"];
	if (mode === "check" || mode === "check-reverse") args.push("--check");
	if (mode === "reverse" || mode === "check-reverse") args.push("--reverse");
	args.push(path.relative(packageRoot, patchPath));
	return args;
}

function runGitApply(packageRoot: string, mode: Exclude<Mode, "status">, quiet = false): GitApplyResult {
	const args = gitApplyArgs(packageRoot, mode);

	const result = spawnSync("git", args, {
		cwd: packageRoot,
		stdio: quiet ? "pipe" : "inherit",
		encoding: "utf8",
	});

	if (result.error) {
		throw result.error;
	}

	return {
		ok: result.status === 0,
		status: result.status,
		stdout: typeof result.stdout === "string" ? result.stdout : "",
		stderr: typeof result.stderr === "string" ? result.stderr : "",
	};
}

function formatFailureDetails(result: GitApplyResult): string {
	const text = [result.stderr, result.stdout].filter(Boolean).join("\n").trim();
	return text ? `\n\n${text}` : "";
}

function logContext(mode: string, ompEntry: string, packageRoot: string): void {
	console.log(`[omp-patch-custom-mcp] mode=${mode}`);
	console.log(`[omp-patch-custom-mcp] ompEntry=${ompEntry}`);
	console.log(`[omp-patch-custom-mcp] packageRoot=${packageRoot}`);
	console.log(`[omp-patch-custom-mcp] patch=${patchPath}`);
	console.log("");
}

function detectPatchState(packageRoot: string): { state: PatchState; details?: string } {
	const canApply = runGitApply(packageRoot, "check", true);
	if (canApply.ok) return { state: "can-apply" };

	const alreadyApplied = runGitApply(packageRoot, "check-reverse", true);
	if (alreadyApplied.ok) return { state: "already-applied" };

	return {
		state: "needs-rebase",
		details: formatFailureDetails(canApply) || formatFailureDetails(alreadyApplied),
	};
}

function handleApplyMode(ompEntry: string, packageRoot: string): number {
	console.log("[omp-patch-custom-mcp] Applying patch...");
	const patchState = detectPatchState(packageRoot);
	logContext("apply", ompEntry, packageRoot);

	if (patchState.state === "already-applied") {
		console.log("[omp-patch-custom-mcp] Patch is already applied.");
		return EXIT_OK;
	}

	if (patchState.state === "needs-rebase") {
		throw new Error(
			`Patch cannot be applied cleanly and does not look already applied. It likely needs a manual rebase.${patchState.details ?? ""}`,
		);
	}

	const applied = runGitApply(packageRoot, "apply", true);
	if (!applied.ok) {
		throw new Error(
			`git ${gitApplyArgs(packageRoot, "apply").join(" ")} failed with exit code ${applied.status ?? "unknown"}${formatFailureDetails(applied)}`,
		);
	}

	console.log("");
	console.log("[omp-patch-custom-mcp] Patch applied.");
	return EXIT_OK;
}

function handleReverseMode(ompEntry: string, packageRoot: string): number {
	console.log("[omp-patch-custom-mcp] Reversing patch...");
	const patchState = detectPatchState(packageRoot);
	logContext("reverse", ompEntry, packageRoot);

	if (patchState.state === "can-apply") {
		console.log("[omp-patch-custom-mcp] Patch is not currently applied.");
		return EXIT_OK;
	}

	if (patchState.state === "needs-rebase") {
		throw new Error(
			`Patch cannot be reversed cleanly because the target does not match either known state. It likely needs manual inspection.${patchState.details ?? ""}`,
		);
	}

	const reversed = runGitApply(packageRoot, "reverse", true);
	if (!reversed.ok) {
		throw new Error(
			`git ${gitApplyArgs(packageRoot, "reverse").join(" ")} failed with exit code ${reversed.status ?? "unknown"}${formatFailureDetails(reversed)}`,
		);
	}

	console.log("");
	console.log("[omp-patch-custom-mcp] Patch reversed.");
	return EXIT_OK;
}

function handleStatusMode(ompEntry: string, packageRoot: string): number {
	console.log("[omp-patch-custom-mcp] Checking patch status...");
	const patchState = detectPatchState(packageRoot);
	logContext("status", ompEntry, packageRoot);

	if (patchState.state === "can-apply") {
		console.log("[omp-patch-custom-mcp] Status: patch can be applied.");
		return EXIT_OK;
	}

	if (patchState.state === "already-applied") {
		console.log("[omp-patch-custom-mcp] Status: patch is already applied.");
		return EXIT_OK;
	}

	console.log("[omp-patch-custom-mcp] Status: patch needs manual rebase.");
	if (patchState.details) console.log(patchState.details.trimStart());
	return EXIT_NEEDS_REBASE;
}

function handleDirectCheckMode(
	ompEntry: string,
	packageRoot: string,
	mode: "check" | "check-reverse",
	label: string,
 ): number {
	console.log(`[omp-patch-custom-mcp] ${label}`);
	logContext(mode, ompEntry, packageRoot);
	const result = runGitApply(packageRoot, mode, true);
	if (!result.ok) {
		throw new Error(
			`git ${gitApplyArgs(packageRoot, mode).join(" ")} failed with exit code ${result.status ?? "unknown"}${formatFailureDetails(result)}`,
		);
	}
	console.log("");
	console.log("[omp-patch-custom-mcp] Done.");
	return EXIT_OK;
}

function main(): void {
	if (!existsSync(patchPath)) {
		throw new Error(`Patch file not found: ${patchPath}`);
	}

	const mode = parseMode(process.argv.slice(2));
	const ompEntry = resolveOmpBinary();
	const packageRoot = findOmpPackageRoot(ompEntry);

	try {
		let exitCode = EXIT_OK;
		if (mode === "apply") {
			exitCode = handleApplyMode(ompEntry, packageRoot);
		} else if (mode === "reverse") {
			exitCode = handleReverseMode(ompEntry, packageRoot);
		} else if (mode === "status") {
			exitCode = handleStatusMode(ompEntry, packageRoot);
		} else if (mode === "check") {
			exitCode = handleDirectCheckMode(
				ompEntry,
				packageRoot,
				"check",
				"Checking whether patch can be applied...",
			);
		} else {
			exitCode = handleDirectCheckMode(
				ompEntry,
				packageRoot,
				"check-reverse",
				"Checking whether patch can be reversed...",
			);
		}
		process.exitCode = exitCode;
	} catch (error) {
		console.error("");
		console.error(
			`[omp-patch-custom-mcp] Failed: ${error instanceof Error ? error.message : String(error)}`,
		);
		process.exitCode = EXIT_GENERIC_FAILURE;
	}
}

main();
