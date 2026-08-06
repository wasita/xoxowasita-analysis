<script lang="ts">
	import { browser } from '$app/environment';
	import cloud from 'd3-cloud';
	import wordsData from '$lib/data/words.json';

	const W = 720;
	const H = 420;
	const max = wordsData.words[0].count;
	const fontSize = (count: number) => 13 + 46 * Math.sqrt(count / max);

	// Three pastel tones from the site palette, by frequency tier.
	const tone = (count: number) =>
		count / max > 0.5 ? '#e879f9' : count / max > 0.15 ? '#a78bfa' : '#8d86a8';

	interface Placed {
		text: string;
		size: number;
		x: number;
		y: number;
		rotate: number;
		count: number;
	}
	let placed = $state<Placed[]>([]);

	if (browser) {
		cloud()
			.size([W, H])
			.words(wordsData.words.map((w) => ({ text: w.text, size: fontSize(w.count), count: w.count })))
			.padding(3)
			.rotate(0)
			.font('system-ui')
			.fontSize((d) => d.size!)
			.random(() => 0.5) // deterministic layout
			.on('end', (out) => (placed = out as Placed[]))
			.start();
	}
</script>

<svg viewBox="0 0 {W} {H}" class="w-full rounded-lg border border-white/10 bg-surface-2/50"
	role="img" aria-label="Most frequent words in the chat">
	<g transform="translate({W / 2},{H / 2})">
		{#each placed as w (w.text)}
			<text
				x={w.x}
				y={w.y}
				text-anchor="middle"
				font-size={w.size}
				font-weight={w.size > 34 ? 700 : 500}
				fill={tone(w.count)}
			>
				{w.text}
				<title>{w.text} ×{w.count}</title>
			</text>
		{/each}
	</g>
</svg>
<p class="mt-2 text-sm text-ink-3">
	Every word used at least twice, sized by frequency (stopwords removed). Hover a word for its
	count.
</p>
