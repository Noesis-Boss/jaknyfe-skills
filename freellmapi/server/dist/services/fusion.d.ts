import { z } from 'zod';
import type { ChatMessage, ChatCompletionResponse } from '@freellmapi/shared/types.js';
import type { CompletionOptions } from '../providers/base.js';
export declare const FUSION_MODEL_ID = "fusion";
export declare function isFusionModel(modelId: string | undefined): boolean;
export declare const fusionConfigSchema: z.ZodObject<{
    models: z.ZodOptional<z.ZodArray<z.ZodString, "many">>;
    k: z.ZodOptional<z.ZodNumber>;
    judge: z.ZodOptional<z.ZodString>;
    strategy: z.ZodOptional<z.ZodEnum<["synthesize", "best_of"]>>;
    expose_panel: z.ZodOptional<z.ZodBoolean>;
}, "strip", z.ZodTypeAny, {
    k?: number | undefined;
    models?: string[] | undefined;
    judge?: string | undefined;
    strategy?: "synthesize" | "best_of" | undefined;
    expose_panel?: boolean | undefined;
}, {
    k?: number | undefined;
    models?: string[] | undefined;
    judge?: string | undefined;
    strategy?: "synthesize" | "best_of" | undefined;
    expose_panel?: boolean | undefined;
}>;
export type FusionConfig = z.infer<typeof fusionConfigSchema>;
export declare function getFusionMaxK(): number;
export declare const savedFusionConfigSchema: z.ZodObject<{
    mode: z.ZodEnum<["auto", "explicit"]>;
    models: z.ZodDefault<z.ZodArray<z.ZodString, "many">>;
    judge: z.ZodDefault<z.ZodNullable<z.ZodString>>;
    k: z.ZodNumber;
    strategy: z.ZodEnum<["synthesize", "best_of"]>;
    expose_panel: z.ZodBoolean;
}, "strip", z.ZodTypeAny, {
    k: number;
    mode: "auto" | "explicit";
    models: string[];
    judge: string | null;
    strategy: "synthesize" | "best_of";
    expose_panel: boolean;
}, {
    k: number;
    mode: "auto" | "explicit";
    strategy: "synthesize" | "best_of";
    expose_panel: boolean;
    models?: string[] | undefined;
    judge?: string | null | undefined;
}>;
export type SavedFusionConfig = z.infer<typeof savedFusionConfigSchema>;
export declare function getSavedFusionConfig(): SavedFusionConfig;
export declare function setSavedFusionConfig(input: SavedFusionConfig): SavedFusionConfig;
/**
 * Merge a request's inline fusion config over the saved dashboard default.
 * Each field present on the request wins; otherwise the saved default applies.
 * An explicit panel only comes from the saved config when its mode is
 * 'explicit' — in 'auto' mode the saved `models` are ignored so the panel is
 * picked fresh off the Fallback Chain.
 */
export declare function resolveEffectiveConfig(req: FusionConfig): FusionConfig;
export interface FusionResult {
    response: ChatCompletionResponse & {
        x_fusion?: unknown;
    };
    routedVia: string;
}
/**
 * Orchestrate a fusion request end to end: select the panel, fan out in
 * parallel, then synthesize survivors with a judge (or best-of). Throws a
 * FusionError when nothing usable comes back so the route can map it to an
 * HTTP status.
 */
export declare class FusionError extends Error {
    status: number;
    constructor(message: string, status: number);
}
export interface FusionHooks {
    onPanel?: (a: {
        platform: string;
        model: string;
        status: 'ok' | 'failed';
        content?: string;
        error?: string;
    }) => void;
    onJudge?: (j: {
        platform: string;
        model: string;
    }) => void;
    onJudgeDelta?: (text: string) => void;
}
export declare function runFusion(params: {
    messages: ChatMessage[];
    config: FusionConfig;
    options: CompletionOptions;
    estimatedTokens: number;
    hooks?: FusionHooks;
}): Promise<FusionResult>;
//# sourceMappingURL=fusion.d.ts.map