<script lang="ts">
	import drift from '$lib/data/drift.json';
	import { segments, EVENT_END_MIN } from '$lib/data';

	const { points, binMinutes } = drift;
	const max = Math.max(...points.map((p) => p.drift));

	const W = 720;
	const H = 220;
	const PAD_L = 36;
	const PAD_B = 24;
	const PAD_T = 16;
	const px = (min: number) => PAD_L + (min / EVENT_END_MIN) * (W - PAD_L);
	const py = (v: number) => PAD_T + (1 - v / max) * (H - PAD_T - PAD_B);

	const line = points
		.map((p, i) => `${i === 0 ? 'M' : 'L'}${px(p.minute + binMinutes / 2).toFixed(1)},${py(p.drift).toFixed(1)}`)
		.join(' ');

	let hover = $state<(typeof points)[number] | null>(null);
	const segmentAt = (min: number) => segments.find((s) => min >= s.start && min < s.end);
</script>

<div class="overflow-x-auto">
	<svg viewBox="0 0 {W} {H}" class="min-w-140 w-full" role="img"
		aria-label="How much the conversation's topic moved, over time">
		<!-- reconstructed section boundaries -->
		{#each segments.slice(1) as s (s.start)}
			<line x1={px(s.start)} y1={PAD_T} x2={px(s.start)} y2={H - PAD_B}
				class="stroke-accent-2" stroke-width="1" stroke-dasharray="3 4" opacity="0.5" />
		{/each}

		<path d={line} fill="none" class="stroke-accent" stroke-width="2" stroke-linejoin="round" />
		{#each points as p (p.minute)}
			<circle
				role="presentation"
				cx={px(p.minute + binMinutes / 2)}
				cy={py(p.drift)}
				r={hover === p ? 6 : 3.5}
				class="fill-accent"
				opacity={hover === null || hover === p ? 0.9 : 0.45}
				onmouseenter={() => (hover = p)}
				onmouseleave={() => (hover = null)}
			/>
		{/each}

		{#each [0, 10, 20, 30, 40, 50, 60, 70] as t}
			<text x={px(t)} y={H - 6} font-size="11" class="fill-ink-3" text-anchor="middle">{t}m</text>
		{/each}
	</svg>
</div>
<p class="mt-1 h-5 text-sm text-ink-2">
	{#if hover}
		<span class="text-accent-soft font-medium">min {hover.minute}–{hover.minute + binMinutes}</span>
		· drift {hover.drift.toFixed(2)}
		{#if segmentAt(hover.minute)}· entering “{segmentAt(hover.minute)?.title}”{/if}
	{:else}
		<span class="text-ink-3">1 − cosine similarity between consecutive 2-minute windows of message embeddings — spikes mean the room changed subject. Dashed lines: the reconstructed talk sections, derived independently.</span>
	{/if}
</p>
