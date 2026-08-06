<script lang="ts">
	import sentiment from '$lib/data/sentiment.json';
	import { messages, EVENT_END_MIN, fmtClock } from '$lib/data';

	const msgById = new Map(messages.map((m) => [m.id, m]));
	const { bins, binMinutes, overallMean } = sentiment;
	const filled = bins.filter((b) => b.mean !== null) as { minute: number; mean: number; n: number }[];

	const W = 720;
	const H = 240;
	const PAD_L = 40;
	const PAD_B = 24;
	const PAD_T = 12;
	const px = (min: number) => PAD_L + (min / EVENT_END_MIN) * (W - PAD_L);
	// y domain fixed to [-1, 1]: VADER compound range, zero line centered
	const py = (v: number) => PAD_T + ((1 - v) / 2) * (H - PAD_T - PAD_B);

	const line = filled
		.map((b, i) => `${i === 0 ? 'M' : 'L'}${px(b.minute + binMinutes / 2).toFixed(1)},${py(b.mean).toFixed(1)}`)
		.join(' ');

	let hover = $state<(typeof filled)[number] | null>(null);
</script>

<div class="overflow-x-auto">
	<svg viewBox="0 0 {W} {H}" class="min-w-140 w-full" role="img"
		aria-label="Average message sentiment across the talk">
		<!-- zero line + guides -->
		{#each [1, 0.5, 0, -0.5, -1] as v}
			<line x1={PAD_L} y1={py(v)} x2={W} y2={py(v)} class={v === 0 ? 'stroke-ink-3' : 'stroke-grid'} stroke-width="1" />
			<text x={PAD_L - 6} y={py(v) + 3.5} font-size="10" text-anchor="end" class="fill-ink-3">{v > 0 ? '+' : ''}{v}</text>
		{/each}

		<path d={line} fill="none" class="stroke-accent" stroke-width="2" stroke-linejoin="round" />
		{#each filled as b (b.minute)}
			<circle
				role="presentation"
				cx={px(b.minute + binMinutes / 2)}
				cy={py(b.mean)}
				r={hover === b ? 6 : 3.5}
				class="fill-accent"
				opacity={hover === null || hover === b ? 0.9 : 0.45}
				onmouseenter={() => (hover = b)}
				onmouseleave={() => (hover = null)}
			>
				<title>min {b.minute}–{b.minute + binMinutes}: {b.mean > 0 ? '+' : ''}{b.mean} across {b.n} messages</title>
			</circle>
		{/each}

		{#each [0, 10, 20, 30, 40, 50, 60, 70] as t}
			<text x={px(t)} y={H - 6} font-size="11" class="fill-ink-3" text-anchor="middle">{t}m</text>
		{/each}
	</svg>
</div>
<p class="mt-1 h-5 text-sm text-ink-2">
	{#if hover}
		<span class="text-accent-soft font-medium">min {hover.minute}–{hover.minute + binMinutes}</span>
		· mean {hover.mean > 0 ? '+' : ''}{hover.mean} across {hover.n} messages
	{:else}
		<span class="text-ink-3">VADER compound per message, averaged per 2 minutes · whole-event mean {overallMean > 0 ? '+' : ''}{overallMean}</span>
	{/if}
</p>

<div class="mt-5 grid gap-4 sm:grid-cols-2">
	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="text-sm font-semibold text-accent-soft">Sweetest, per the algorithm</h3>
		<ul class="mt-3 space-y-2 text-sm text-ink-2">
			{#each sentiment.mostPositive as id (id)}
				{@const m = msgById.get(id)}
				{#if m}
					<li><span class="font-medium text-ink">{m.name}</span> <span class="text-ink-3">({fmtClock(m.minutes)})</span>: {m.text}</li>
				{/if}
			{/each}
		</ul>
	</div>
	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="text-sm font-semibold text-accent-2">Grumpiest, per the algorithm</h3>
		<ul class="mt-3 space-y-2 text-sm text-ink-2">
			{#each sentiment.mostNegative as id (id)}
				{@const m = msgById.get(id)}
				{#if m}
					<li><span class="font-medium text-ink">{m.name}</span> <span class="text-ink-3">({fmtClock(m.minutes)})</span>: {m.text}</li>
				{/if}
			{/each}
		</ul>
		<p class="mt-3 text-xs text-ink-3">
			Yes, “CRUSHED IT!!!” ranks as negative — sentiment models take “crushed” literally.
			Affectionate roasting suffers the same fate.
		</p>
	</div>
</div>
