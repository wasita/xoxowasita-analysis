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
			<li class="grid grid-cols-[9.5rem_1fr_3rem] items-center gap-2 text-sm">
				<span class="whitespace-nowrap text-ink-2">{a.name}</span>
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
		How it's computed: take the time gaps between each of a person's messages, then compare
		how uneven those gaps are (their standard deviation σ) to their average length (μ):
		B&nbsp;=&nbsp;(σ&nbsp;−&nbsp;μ)&nbsp;/&nbsp;(σ&nbsp;+&nbsp;μ), the Goh–Barabási burstiness
		index. Perfectly even gaps give −1 (a metronome), random timing gives ≈ 0, and long
		silences broken by rapid flurries push toward +1. Everyone with ≥ {minMessages} messages
		during the live event.
	</p>
</div>
