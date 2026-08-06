<script lang="ts">
	import matrix from '$lib/data/matrix.json';

	const { names, cells } = matrix;
	const n = names.length;
	const max = Math.max(...cells.flat());

	const CELL = 34;
	const GUTTER = 110;
	const W = GUTTER + n * CELL;
	const H = GUTTER + n * CELL;

	let hover = $state<{ g: number; r: number } | null>(null);
</script>

<div class="overflow-x-auto">
	<svg viewBox="0 0 {W} {H}" class="w-full min-w-140" role="img"
		aria-label="Matrix of who reacted to whose messages">
		{#each names as giver, g (giver)}
			<text
				x={GUTTER - 8}
				y={GUTTER + g * CELL + CELL / 2 + 4}
				text-anchor="end"
				font-size="11"
				class="fill-ink-2"
				opacity={hover === null || hover.g === g ? 1 : 0.35}
			>{giver}</text>
		{/each}
		{#each names as receiver, r (receiver)}
			<text
				transform="rotate(-45 {GUTTER + r * CELL + CELL / 2} {GUTTER - 8})"
				x={GUTTER + r * CELL + CELL / 2}
				y={GUTTER - 8}
				font-size="11"
				class="fill-ink-2"
				opacity={hover === null || hover.r === r ? 1 : 0.35}
			>{receiver}</text>
		{/each}
		{#each cells as row, g}
			{#each row as count, r}
				<rect
					role="presentation"
					x={GUTTER + r * CELL + 1}
					y={GUTTER + g * CELL + 1}
					width={CELL - 2}
					height={CELL - 2}
					rx="4"
					class="fill-accent"
					opacity={count === 0 ? 0.04 : 0.15 + 0.85 * (count / max)}
					stroke={hover && hover.g === g && hover.r === r ? 'var(--color-accent-2)' : 'none'}
					stroke-width="2"
					onmouseenter={() => (hover = { g, r })}
					onmouseleave={() => (hover = null)}
				/>
				{#if count >= 5}
					<text
						x={GUTTER + r * CELL + CELL / 2}
						y={GUTTER + g * CELL + CELL / 2 + 4}
						text-anchor="middle"
						font-size="11"
						class="pointer-events-none fill-ink"
					>{count}</text>
				{/if}
			{/each}
		{/each}
	</svg>
</div>
<p class="mt-1 h-5 text-sm text-ink-2">
	{#if hover}
		<span class="text-accent-soft font-medium">{names[hover.g]}</span>
		gave {cells[hover.g][hover.r]} reaction{cells[hover.g][hover.r] === 1 ? '' : 's'} to
		<span class="text-accent-soft font-medium">{names[hover.r]}</span>
	{:else}
		<span class="text-ink-3">rows give, columns receive — the {names.length} most reaction-involved people. Darker = more reactions.</span>
	{/if}
</p>
