<script lang="ts">
	import affect from '$lib/data/affect.json';
	import { EVENT_END_MIN } from '$lib/data';

	const { families, binMinutes } = affect;
	const maxBin = Math.max(...families.flatMap((f) => f.bins));

	const W = 720;
	const ROW_H = 64;
	const WAVE_H = 46;
	const LEFT = 130;
	const H = families.length * ROW_H;

	const px = (bin: number, nBins: number) => LEFT + (bin / (nBins - 1)) * (W - LEFT);

	const areaPath = (bins: number[], baseY: number) => {
		const pts = bins.map(
			(v, i) => `${px(i, bins.length).toFixed(1)},${(baseY - (v / maxBin) * WAVE_H).toFixed(1)}`
		);
		return `M${LEFT},${baseY} L${pts.join(' L')} L${W},${baseY} Z`;
	};

	let hover = $state<{ label: string; count: number; minute: number } | null>(null);
	const nBins = families[0].bins.length;
</script>

<div class="overflow-x-auto">
	<svg viewBox="0 0 {W} {H + 24}" class="min-w-140 w-full" role="img"
		aria-label="Emoji reactions grouped by feeling, over the course of the talk">
		{#each families as f, i (f.key)}
			{@const baseY = (i + 1) * ROW_H - 8}
			<text x="0" y={baseY - 18} font-size="16">{f.glyph}</text>
			<text x="26" y={baseY - 16} font-size="12" class="fill-ink-2">{f.label}</text>
			<text x="26" y={baseY - 2} font-size="11" class="fill-ink-3">×{f.total}</text>
			<line x1={LEFT} y1={baseY} x2={W} y2={baseY} class="stroke-grid" stroke-width="1" />
			<path d={areaPath(f.bins, baseY)} class="fill-accent" opacity="0.55" />
			<!-- invisible hover strips -->
			{#each f.bins as count, b}
				<rect
					role="presentation"
					x={px(b, nBins) - (W - LEFT) / nBins / 2}
					y={baseY - ROW_H + 10}
					width={(W - LEFT) / nBins}
					height={ROW_H - 10}
					fill="transparent"
					onmouseenter={() => (hover = { label: `${f.glyph} ${f.label}`, count, minute: b * binMinutes })}
					onmouseleave={() => (hover = null)}
				/>
			{/each}
		{/each}
		{#each [0, 10, 20, 30, 40, 50, 60, 70] as t}
			<text x={LEFT + (t / EVENT_END_MIN) * (W - LEFT)} y={H + 16} font-size="11"
				class="fill-ink-3" text-anchor="middle">{t}m</text>
		{/each}
	</svg>
</div>
<p class="mt-1 h-5 text-sm text-ink-2">
	{#if hover}
		<span class="text-accent-soft font-medium">{hover.label}</span>
		×{hover.count} around minute {hover.minute}–{hover.minute + binMinutes}
	{:else}
		<span class="text-ink-3">every reaction emoji mapped to a feeling — same scale across rows, {affect.unmapped} reactions unmapped</span>
	{/if}
</p>
