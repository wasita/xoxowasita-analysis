<script lang="ts">
	import burstiness from '$lib/data/burstiness.json';

	const { authors, minMessages } = burstiness;
	const maxAbs = Math.max(...authors.map((a) => Math.abs(a.b)));
</script>

<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
	<div class="mb-2 flex justify-between text-xs text-ink-3">
		<span>← steady drumbeat</span>
		<span>silence, then a flurry →</span>
	</div>
	<ol class="space-y-2">
		{#each authors as a (a.name)}
			<li class="grid grid-cols-[7rem_1fr_3rem] items-center gap-2 text-sm">
				<span class="truncate text-ink-2" title={a.name}>{a.name}</span>
				<div class="relative h-3.5">
					<div class="absolute inset-y-0 left-1/2 w-px bg-white/20"></div>
					<div
						class="absolute inset-y-0 rounded-[4px] {a.b >= 0 ? 'left-1/2 bg-accent' : 'bg-accent-2'}"
						style={a.b >= 0
							? `width: ${(a.b / maxAbs) * 50}%`
							: `right: 50%; width: ${(-a.b / maxAbs) * 50}%`}
					></div>
				</div>
				<span class="text-right text-ink-2" style="font-variant-numeric: tabular-nums"
					>{a.b > 0 ? '+' : ''}{a.b.toFixed(2)}</span>
			</li>
		{/each}
	</ol>
	<p class="mt-4 text-sm text-ink-3">
		Goh–Barabási burstiness of each person's gaps between messages (−1 = metronome,
		0 = random, +1 = long silences broken by flurries). Everyone with ≥ {minMessages} messages
		during the live event.
	</p>
</div>
