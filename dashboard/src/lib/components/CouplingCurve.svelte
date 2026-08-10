<script lang="ts">
	import coupling from '$lib/data/coupling.json';
	import { messages, fmtClock } from '$lib/data';

	const msgById = new Map(messages.map((m) => [m.id, m]));
	const { bins, binMinutes, people, overallMean } = coupling;
	const filled = bins.filter((b) => b.mean !== null) as { minute: number; mean: number; n: number }[];
	const maxMean = Math.max(...filled.map((b) => b.mean));

	const W = 720;
	const H = 220;
	const PAD_L = 40;
	const PAD_B = 24;
	const PAD_T = 12;
	const X_MAX = 68;
	const px = (min: number) => PAD_L + (min / X_MAX) * (W - PAD_L);
	const py = (v: number) => PAD_T + (1 - v / maxMean) * (H - PAD_T - PAD_B);

	const line = filled
		.map((b, i) => `${i === 0 ? 'M' : 'L'}${px(b.minute + binMinutes / 2).toFixed(1)},${py(b.mean).toFixed(1)}`)
		.join(' ');

	let hover = $state<(typeof filled)[number] | null>(null);
	const maxPerson = people[0].mean;
</script>

<div class="overflow-x-auto">
	<svg viewBox="0 0 {W} {H}" class="min-w-140 w-full" role="img"
		aria-label="How closely chat messages tracked what was being said on stage">
		{#each [0, 0.1, 0.2, 0.3] as v}
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
				class="fill-accent"
				opacity={hover === null || hover === b ? 0.9 : 0.45}
				onmouseenter={() => (hover = b)}
				onmouseleave={() => (hover = null)}
			/>
		{/each}
		{#each [0, 10, 20, 30, 40, 50, 60] as t}
			<text x={px(t)} y={H - 6} font-size="11" class="fill-ink-3" text-anchor="middle">{t}m</text>
		{/each}
	</svg>
</div>
<p class="mt-1 h-5 text-sm text-ink-2">
	{#if hover}
		<span class="text-accent-soft font-medium">min {hover.minute}–{hover.minute + binMinutes}</span>
		· mean coupling {hover.mean.toFixed(2)} across {hover.n} messages
	{:else}
		<span class="text-ink-3">semantic similarity between each message and the words spoken on stage in that moment (same method as study 2, same embedding model) · whole-talk mean {overallMean.toFixed(2)}</span>
	{/if}
</p>

<div class="mt-5 grid gap-4 lg:grid-cols-2">
	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="font-semibold text-ink">Most on-topic commentators</h3>
		<ol class="mt-4 space-y-2.5">
			{#each people.slice(0, 8) as p (p.name)}
				<li class="grid grid-cols-[9.5rem_1fr_3rem] items-center gap-2 text-sm">
					<span class="whitespace-nowrap text-ink-2">{p.name}</span>
					<div class="h-3.5 overflow-hidden rounded-[4px] bg-white/5">
						<div class="h-full rounded-[4px] bg-accent" style="width: {(p.mean / maxPerson) * 100}%"></div>
					</div>
					<span class="text-right text-ink-2" style="font-variant-numeric: tabular-nums">{p.mean.toFixed(2)}</span>
				</li>
			{/each}
		</ol>
		<p class="mt-3 text-xs text-ink-3">mean coupling, everyone with ≥ 5 scored messages — lower half of this list = beloved chaos agents</p>
	</div>
	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="font-semibold text-ink">Closest echoes of the talk</h3>
		<ul class="mt-4 space-y-3 text-sm">
			{#each coupling.mostCoupled.slice(0, 4) as id (id)}
				{@const m = msgById.get(id)}
				{#if m}
					<li>
						<span class="font-medium text-accent-soft">{m.name}</span>
						<span class="text-ink-3"> ({fmtClock(m.minutes)})</span>: <span class="text-ink">{m.text}</span>
					</li>
				{/if}
			{/each}
		</ul>
		<p class="mt-3 text-xs text-ink-3">the messages that most precisely mirrored what was being said on stage as they were sent</p>
	</div>
</div>
