<script lang="ts">
	import { AreaChart } from 'layerchart';
	import { perMinute, segments } from '$lib/data';

	let active = $state<number | null>(null);
</script>

<div class="h-72">
	<AreaChart
		data={perMinute}
		x="minute"
		y="messages"
		series={[{ key: 'messages', label: 'messages / min', color: 'var(--color-accent)' }]}
	/>
</div>

<!-- Segment strip: the reconstructed talk sections, aligned to the same time axis -->
<div class="mt-3">
	<div class="flex h-8 overflow-hidden rounded-md border border-white/10">
		{#each segments as seg, i (seg.start)}
			<a
				href="#segment-{i}"
				class="group relative block h-full border-r border-white/10 last:border-r-0 transition-colors
				       {i % 2 === 0 ? 'bg-surface-2' : 'bg-surface'}
				       hover:bg-accent/30"
				style="width: {((seg.end - seg.start) / segments[segments.length - 1].end) * 100}%"
				onmouseenter={() => (active = i)}
				onmouseleave={() => (active = null)}
				aria-label={seg.title}
			></a>
		{/each}
	</div>
	<p class="mt-2 h-5 text-sm text-ink-2">
		{#if active !== null}
			<span class="text-accent-soft font-medium">{Math.round(segments[active].start)}–{Math.round(segments[active].end)} min</span>
			· {segments[active].title}
		{:else}
			<span class="text-ink-3">hover the strip — each block is a reconstructed section of the talk (click to jump)</span>
		{/if}
	</p>
</div>
