export interface EmbeddingModelRow {
    id: number;
    family: string;
    platform: string;
    model_id: string;
    display_name: string;
    dimensions: number;
    max_input_tokens: number | null;
    priority: number;
    enabled: number;
    quota_label: string;
}
export interface EmbeddingsResult {
    family: string;
    platform: string;
    modelId: string;
    dimensions: number;
    vectors: number[][];
    inputTokens: number;
}
export declare class EmbeddingsError extends Error {
    status: number;
    constructor(message: string, status: number);
}
export declare function listEmbeddingModels(): EmbeddingModelRow[];
export declare function getDefaultFamily(): string;
/** Map the request's `model` to a family: 'auto'/empty → default; a family
 * name → itself; a provider-specific model id → its family. */
export declare function resolveFamily(model: string | undefined): string | null;
/** Embed `inputs` via the family's provider chain, failing over within the
 * family on any provider error. Throws EmbeddingsError when the chain is dry. */
export declare function runEmbeddings(model: string | undefined, inputs: string[]): Promise<EmbeddingsResult>;
//# sourceMappingURL=embeddings.d.ts.map