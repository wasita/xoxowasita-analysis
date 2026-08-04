<script lang="ts">
	import { points, topics, messages } from '$lib/data';

	const msgById = new Map(messages.map((m) => [m.id, m]));

	const topicCounts = Object.fromEntries(
		Object.keys(topics).map((t) => [t, points.filter((p) => p.topic === t).length])
	);
	const topicOrder = Object.keys(topics).sort((a, b) => topicCounts[b] - topicCounts[a]);

	let selected = $state<string | null>(null);
	let hover = $state<string | null>(null);

	const W = 720;
	const H = 480;
	const PAD = 20;
	const xs = points.map((p) => p.x);
	const ys = points.map((p) => p.y);
	const [x0, x1] = [Math.min(...xs), Math.max(...xs)];
	const [y0, y1] = [Math.min(...ys), Math.max(...ys)];
	const sx = (x: number) => PAD + ((x - x0) / (x1 - x0)) * (W - 2 * PAD);
	const sy = (y: number) => PAD + ((y1 - y) / (y1 - y0)) * (H - 2 * PAD);

	const hoverMsg = $derived(hover ? msgById.get(hover) : null);
</script>

<div class="mb-3 flex flex-wrap gap-1.5">
	<button
		class="rounded-full border px-3 py-1 text-sm transition-colors
		       {selected === null
			? 'border-accent bg-accent/20 text-ink'
			: 'border-white/10 text-ink-2 hover:border-white/25'}"
		onclick={() => (selected = null)}
	>
		all topics
	</button>
	{#each topicOrder as t (t)}
		<button
			class="rounded-full border px-3 py-1 text-sm transition-colors
			       {selected === t
				? 'border-accent bg-accent/20 text-ink'
				: 'border-white/10 text-ink-2 hover:border-white/25'}"
			onclick={() => (selected = selected === t ? null : t)}
		>
			{topics[t].label} <span class="text-ink-3">{topicCounts[t]}</span>
		</button>
	{/each}
</div>

<div class="relative">
	<svg viewBox="0 0 {W} {H}" class="w-full rounded-lg border border-white/10 bg-surface-2/50"
		role="img" aria-label="Semantic map of all 340 messages; nearby messages say similar things">
		{#each points as p (p.id)}
			{@const dim = selected !== null && p.topic !== selected}
			<circle
				role="presentation"
				cx={sx(p.x)}
				cy={sy(p.y)}
				r={hover === p.id ? 8 : dim ? 3 : 4.5}
				class={dim ? 'fill-ink-3' : 'fill-accent'}
				opacity={dim ? 0.25 : hover === p.id ? 1 : 0.8}
				onmouseenter={() => (hover = p.id)}
				onmouseleave={() => (hover = null)}
			/>
		{/each}
	</svg>
	{#if hoverMsg}
		<div
			class="pointer-events-none absolute bottom-3 left-3 right-3 rounded-lg border border-white/15 bg-page/95 px-4 py-3 shadow-xl"
		>
			<p class="text-sm">
				<span class="font-semibold text-accent-soft">{hoverMsg.name}</span>
				<span class="text-ink-3"> · min {Math.round(hoverMsg.minutes)} · {topics[hoverMsg.topic].label}</span>
			</p>
			<p class="mt-0.5 text-sm text-ink-2">{hoverMsg.text}</p>
		</div>
	{/if}
</div>
<p class="mt-2 text-sm text-ink-3">
	Each dot is one message, placed by meaning (MiniLM embeddings → UMAP). Pick a topic to light
	up its messages; hover any dot to read it.
</p>
