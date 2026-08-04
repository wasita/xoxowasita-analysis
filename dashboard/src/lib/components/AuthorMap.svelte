<script lang="ts">
	import authorsData from '$lib/data/authors.json';

	const { authors, minMessages } = authorsData;

	const W = 720;
	const H = 460;
	const PAD = 48;
	const xs = authors.map((a) => a.x);
	const ys = authors.map((a) => a.y);
	const [x0, x1] = [Math.min(...xs), Math.max(...xs)];
	const [y0, y1] = [Math.min(...ys), Math.max(...ys)];
	const sx = (x: number) => PAD + ((x - x0) / (x1 - x0)) * (W - 2 * PAD);
	const sy = (y: number) => PAD + ((y1 - y) / (y1 - y0)) * (H - 2 * PAD);
	const radius = (n: number) => 4 + 3 * Math.sqrt(n);

	let hover = $state<string | null>(null);
	const hoverAuthor = $derived(hover ? authors.find((a) => a.name === hover) : null);

	const labeled = new Set(
		[...authors].sort((a, b) => b.messages - a.messages).slice(0, 16).map((a) => a.name)
	);
</script>

<div class="relative">
	<svg viewBox="0 0 {W} {H}" class="w-full rounded-lg border border-white/10 bg-surface-2/50"
		role="img" aria-label="Map of authors by writing style similarity">
		{#each authors as a (a.name)}
			<circle
				role="presentation"
				cx={sx(a.x)}
				cy={sy(a.y)}
				r={radius(a.messages)}
				class={hover === a.name ? 'fill-accent-2' : 'fill-accent'}
				opacity={hover === null || hover === a.name ? 0.85 : 0.3}
				onmouseenter={() => (hover = a.name)}
				onmouseleave={() => (hover = null)}
			/>
			{#if labeled.has(a.name) || hover === a.name}
				<text
					x={sx(a.x)}
					y={sy(a.y) - radius(a.messages) - 4}
					text-anchor="middle"
					font-size="11"
					class="pointer-events-none fill-ink-2"
				>{a.name}</text>
			{/if}
		{/each}
	</svg>
	{#if hoverAuthor}
		<div class="pointer-events-none absolute bottom-3 left-3 right-3 rounded-lg border border-white/15 bg-page/95 px-4 py-3 shadow-xl">
			<p class="text-sm">
				<span class="font-semibold text-accent-soft">{hoverAuthor.name}</span>
				<span class="text-ink-3">
					· {hoverAuthor.messages} messages · style twin: {hoverAuthor.styleTwin}</span>
			</p>
			<p class="mt-1 text-sm text-ink-2">
				{#each hoverAuthor.traits as t, i (t.text)}{i > 0 ? ' · ' : ''}{t.text}{/each}
			</p>
			<p class="mt-1 text-sm text-ink-3">most-reacted: “{hoverAuthor.sample}”</p>
		</div>
	{/if}
</div>
<p class="mt-2 text-sm text-ink-3">
	Placed by <em>how</em> they type, not what they said: CAPS, !!!, letter-stretching, lol/haha,
	slang, …-pauses, emoji, pronouns and articles — z-scored across the room, laid out with UMAP.
	Neighbors share a voice; dot size = message count. Everyone with ≥ {minMessages} messages
	(or ≥ {authorsData.minWords} words). Hover for each person's signature moves and style twin.
</p>
