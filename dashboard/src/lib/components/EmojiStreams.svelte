<script lang="ts">
	import { emojiRows, EMOJI_BIN_MIN, EVENT_END_MIN } from '$lib/data';

	const rows = emojiRows.slice(0, 10);
	const maxBin = Math.max(...rows.flatMap((r) => r.bins));
	const nBins = rows[0].bins.length;

	const W = 720;
	const ROW_H = 34;
	const LEFT = 76; // emoji + total gutter
	const H = rows.length * ROW_H;

	const cx = (bin: number) => LEFT + ((bin + 0.5) / nBins) * (W - LEFT);
	const r = (count: number) => (count > 0 ? 3 + 9 * Math.sqrt(count / maxBin) : 0);

	let hover = $state<{ emoji: string; count: number; minute: number } | null>(null);
</script>

<div class="overflow-x-auto">
	<svg viewBox="0 0 {W} {H + 24}" class="min-w-140 w-full" role="img"
		aria-label="When each emoji reaction happened during the talk">
		{#each rows as row, i (row.emoji)}
			{@const y = i * ROW_H + ROW_H / 2}
			<text x="0" y={y + 6} font-size="17">{row.emoji}</text>
			<text x="30" y={y + 5} font-size="12" class="fill-ink-3" font-variant="tabular-nums">
				×{row.total}
			</text>
			<line x1={LEFT} y1={y} x2={W} y2={y} class="stroke-grid" stroke-width="1" />
			{#each row.bins as count, b}
				{#if count > 0}
					<circle
						role="presentation"
						cx={cx(b)}
						cy={y}
						r={r(count)}
						class="fill-accent transition-opacity"
						opacity={hover && hover.emoji !== row.emoji ? 0.25 : 0.85}
						onmouseenter={() => (hover = { emoji: row.emoji, count, minute: b * EMOJI_BIN_MIN })}
						onmouseleave={() => (hover = null)}
					>
						<title>{row.emoji} ×{count} around minute {b * EMOJI_BIN_MIN}–{b * EMOJI_BIN_MIN + EMOJI_BIN_MIN}</title>
					</circle>
				{/if}
			{/each}
		{/each}
		<!-- time axis -->
		{#each [0, 10, 20, 30, 40, 50, 60, 70] as t}
			<text x={LEFT + (t / EVENT_END_MIN) * (W - LEFT)} y={H + 18} font-size="11"
				class="fill-ink-3" text-anchor="middle">{t}m</text>
		{/each}
	</svg>
</div>
<p class="mt-1 h-5 text-sm text-ink-2">
	{#if hover}
		<span class="text-accent-soft font-medium">{hover.emoji} ×{hover.count}</span>
		around minute {hover.minute}–{hover.minute + EMOJI_BIN_MIN}
	{:else}
		<span class="text-ink-3">bubble size = reactions in a 2-minute window (timed by the message reacted to)</span>
	{/if}
</p>
