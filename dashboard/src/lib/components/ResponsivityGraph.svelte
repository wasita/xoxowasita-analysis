<script lang="ts">
	import responsivity from '$lib/data/responsivity.json';

	const { nodes, edges } = responsivity;
	const byName = new Map(nodes.map((n) => [n.name, n]));
	const maxCount = edges[0].count;

	const W = 720;
	const H = 520;
	const PAD = 52;
	const xs = nodes.map((n) => n.x);
	const ys = nodes.map((n) => n.y);
	const [x0, x1] = [Math.min(...xs), Math.max(...xs)];
	const [y0, y1] = [Math.min(...ys), Math.max(...ys)];
	const sx = (x: number) => PAD + ((x - x0) / (x1 - x0)) * (W - 2 * PAD);
	const sy = (y: number) => PAD + ((y1 - y) / (y1 - y0)) * (H - 2 * PAD);
	const radius = (turns: number) => 4 + 2 * Math.sqrt(turns);

	// Curved directed edge: bow to the right of travel so A→B and B→A separate.
	const path = (a: string, b: string) => {
		const s = byName.get(a)!;
		const t = byName.get(b)!;
		const x1p = sx(s.x), y1p = sy(s.y), x2p = sx(t.x), y2p = sy(t.y);
		const dx = x2p - x1p, dy = y2p - y1p;
		const len = Math.hypot(dx, dy) || 1;
		const mx = (x1p + x2p) / 2 + (dy / len) * 16;
		const my = (y1p + y2p) / 2 - (dx / len) * 16;
		// stop short of the target node so the arrowhead shows
		const tEnd = 1 - (radius(t.turns) + 6) / len;
		const qx = (u: number) => (1 - u) ** 2 * x1p + 2 * (1 - u) * u * mx + u ** 2 * x2p;
		const qy = (u: number) => (1 - u) ** 2 * y1p + 2 * (1 - u) * u * my + u ** 2 * y2p;
		return `M${x1p},${y1p} Q${mx},${my} ${qx(tEnd)},${qy(tEnd)}`;
	};

	let hover = $state<string | null>(null);
	const hoverNode = $derived(hover ? byName.get(hover) : null);
	const respondsTo = $derived(
		hover ? edges.filter((e) => e.source === hover).sort((a, b) => b.count - a.count) : []
	);
	const respondedBy = $derived(
		hover ? edges.filter((e) => e.target === hover).sort((a, b) => b.count - a.count) : []
	);
</script>

<div class="relative">
	<svg viewBox="0 0 {W} {H}" class="w-full rounded-lg border border-white/10 bg-surface-2/50"
		role="img" aria-label="Directed graph of who speaks right after whom more than chance">
		<defs>
			<marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
				<path d="M0,0 L8,4 L0,8 z" fill="var(--color-accent)" />
			</marker>
			<marker id="arrow-hot" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
				<path d="M0,0 L8,4 L0,8 z" fill="var(--color-accent-2)" />
			</marker>
		</defs>
		{#each edges as e (e.source + '→' + e.target)}
			{@const lit = hover !== null && (e.source === hover || e.target === hover)}
			<path
				d={path(e.source, e.target)}
				fill="none"
				class={lit ? 'stroke-accent-2' : 'stroke-accent'}
				stroke-width={0.8 + 3.5 * (e.count / maxCount)}
				opacity={hover === null ? (e.z >= 1.64 ? 0.7 : 0.15) : lit ? 0.95 : 0.05}
				marker-end={lit ? 'url(#arrow-hot)' : 'url(#arrow)'}
			/>
		{/each}
		{#each nodes as n (n.name)}
			{@const dim =
				hover !== null &&
				hover !== n.name &&
				!edges.some((e) => (e.source === hover && e.target === n.name) || (e.target === hover && e.source === n.name))}
			<circle
				role="presentation"
				cx={sx(n.x)}
				cy={sy(n.y)}
				r={radius(n.turns)}
				class={hover === n.name ? 'fill-accent-2' : 'fill-accent'}
				opacity={dim ? 0.2 : 0.9}
				onmouseenter={() => (hover = n.name)}
				onmouseleave={() => (hover = null)}
			/>
			<text
				x={sx(n.x)}
				y={sy(n.y) - radius(n.turns) - 4}
				text-anchor="middle"
				font-size="11"
				class="pointer-events-none fill-ink-2"
				opacity={dim ? 0.25 : 1}
			>{n.name}</text>
		{/each}
	</svg>

	{#if hoverNode}
		<div class="pointer-events-none absolute right-3 top-3 w-64 rounded-lg border border-white/15 bg-page/95 px-4 py-3 shadow-xl">
			<p class="font-semibold text-accent-soft">{hoverNode.name}</p>
			{#if respondsTo.length}
				<p class="mt-2 text-xs font-medium text-ink-3 uppercase tracking-wide">jumps in after</p>
				<ul class="mt-1 space-y-0.5 text-xs text-ink-2">
					{#each respondsTo.slice(0, 4) as e (e.target)}
						<li>{e.target} <span class="text-ink-3">— ×{e.count}, {e.ratio}× chance (z {e.z})</span></li>
					{/each}
				</ul>
			{/if}
			{#if respondedBy.length}
				<p class="mt-2 text-xs font-medium text-ink-3 uppercase tracking-wide">gets followed by</p>
				<ul class="mt-1 space-y-0.5 text-xs text-ink-2">
					{#each respondedBy.slice(0, 4) as e (e.source)}
						<li>{e.source} <span class="text-ink-3">— ×{e.count}, {e.ratio}× chance (z {e.z})</span></li>
					{/each}
				</ul>
			{/if}
		</div>
	{/if}
</div>
<p class="mt-2 text-sm text-ink-3">
	An arrow from B to A means B takes the floor right after A. Thickness = how often; solid =
	more often than chance (z ≥ 1.64 against a permutation null that shuffles turn order while
	keeping everyone's number of turns); faint = volume explainable by chattiness alone. Node
	size = turns taken. Hover a person for their conversational orbit.
</p>
