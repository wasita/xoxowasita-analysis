<script lang="ts">
	import togetherness from '$lib/data/togetherness.json';
	import { segments, EVENT_END_MIN } from '$lib/data';

	const { bins, binMinutes, peakMinute, troughMinute, overallMean } = togetherness;
	const filled = bins.filter((b) => b.mean !== null) as { minute: number; mean: number; n: number }[];
	const maxMean = Math.max(...filled.map((b) => b.mean));

	const W = 720;
	const H = 220;
	const PAD_L = 40;
	const PAD_B = 24;
	const PAD_T = 12;
	const px = (min: number) => PAD_L + (min / EVENT_END_MIN) * (W - PAD_L);
	const py = (v: number) => PAD_T + (1 - v / maxMean) * (H - PAD_T - PAD_B);

	const line = filled
		.map((b, i) => `${i === 0 ? 'M' : 'L'}${px(b.minute + binMinutes / 2).toFixed(1)},${py(b.mean).toFixed(1)}`)
		.join(' ');

	let hover = $state<(typeof filled)[number] | null>(null);
	const segmentAt = (min: number) => segments.find((s) => min >= s.start && min < s.end);
</script>

<div class="overflow-x-auto">
	<svg viewBox="0 0 {W} {H}" class="min-w-140 w-full" role="img"
		aria-label="How much different people's messages converged, over time">
		{#each [0, 0.25, 0.5, 0.75] as v}
			{#if v <= maxMean}
				<line x1={PAD_L} y1={py(v)} x2={W} y2={py(v)} class="stroke-grid" stroke-width="1" />
				<text x={PAD_L - 6} y={py(v) + 3.5} font-size="10" text-anchor="end" class="fill-ink-3">{v}</text>
			{/if}
		{/each}
		<path d={line} fill="none" class="stroke-accent" stroke-width="2" stroke-linejoin="round" />
		{#each filled as b (b.minute)}
			<circle
				role="presentation"
				cx={px(b.minute + binMinutes / 2)}
				cy={py(b.mean)}
				r={hover === b ? 6 : 3.5}
				class={b.minute === peakMinute || b.minute === troughMinute ? 'fill-accent-2' : 'fill-accent'}
				opacity={hover === null || hover === b ? 0.9 : 0.45}
				onmouseenter={() => (hover = b)}
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
		· togetherness {hover.mean.toFixed(2)} across {hover.n} messages
		{#if segmentAt(hover.minute)}· “{segmentAt(hover.minute)?.title}”{/if}
	{:else}
		<span class="text-ink-3">mean semantic similarity between different people's messages within each 2-minute window — high = one shared conversation, low = scattered side-chats · pink dots mark the extremes</span>
	{/if}
</p>
<p class="mt-3 text-sm text-ink-2">
	Peak togetherness: minute {peakMinute} — the whole room chanting about Joji in unison.
	Most fragmented: minute {troughMinute}, mid thread-discovery chaos. Event mean
	{overallMean.toFixed(2)}.
</p>
