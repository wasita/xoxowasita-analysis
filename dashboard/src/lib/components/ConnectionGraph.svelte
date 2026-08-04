<script lang="ts">
	import network from '$lib/data/network.json';

	interface Node {
		name: string;
		x: number;
		y: number;
		messages: number;
		reactionsReceived: number;
		reactionsGiven: number;
		degree: number;
		community: number;
	}

	const nodes: Node[] = network.nodes;
	const edges = network.edges;
	const byName = new Map(nodes.map((n) => [n.name, n]));

	const W = 720;
	const H = 560;
	const PAD = 46;
	const xs = nodes.map((n) => n.x);
	const ys = nodes.map((n) => n.y);
	const [x0, x1] = [Math.min(...xs), Math.max(...xs)];
	const [y0, y1] = [Math.min(...ys), Math.max(...ys)];
	const sx = (x: number) => PAD + ((x - x0) / (x1 - x0)) * (W - 2 * PAD);
	const sy = (y: number) => PAD + ((y1 - y) / (y1 - y0)) * (H - 2 * PAD);

	const radius = (n: Node) => 3 + 2.2 * Math.sqrt(n.messages + n.reactionsGiven / 3);
	const maxWeight = edges[0].weight;

	let hover = $state<string | null>(null);

	const touches = (e: (typeof edges)[number], name: string) => e.a === name || e.b === name;
	const hoverNode = $derived(hover ? byName.get(hover) : null);
	const partners = $derived(
		hover
			? edges
					.filter((e) => touches(e, hover!))
					.map((e) => ({ other: e.a === hover ? e.b : e.a, ...e }))
					.slice(0, 6)
			: []
	);

	// Direct labels only where they earn their ink: the most active people.
	const labeled = new Set(
		[...nodes].sort((a, b) => radius(b) - radius(a)).slice(0, 14).map((n) => n.name)
	);
</script>

<div class="relative">
	<svg viewBox="0 0 {W} {H}" class="w-full rounded-lg border border-white/10 bg-surface-2/50"
		role="img" aria-label="Network of who reacted, replied, and mentioned whom">
		{#each edges as e (e.a + e.b)}
			{@const lit = hover !== null && touches(e, hover)}
			<line
				x1={sx(byName.get(e.a)!.x)}
				y1={sy(byName.get(e.a)!.y)}
				x2={sx(byName.get(e.b)!.x)}
				y2={sy(byName.get(e.b)!.y)}
				class={lit ? 'stroke-accent-2' : 'stroke-accent'}
				stroke-width={lit ? 1.6 : 0.6 + 2.4 * (e.weight / maxWeight)}
				opacity={hover === null ? 0.1 + 0.35 * (e.weight / maxWeight) : lit ? 0.9 : 0.04}
			/>
		{/each}
		{#each nodes as n (n.name)}
			{@const dim = hover !== null && hover !== n.name && !edges.some((e) => touches(e, hover!) && touches(e, n.name))}
			<circle
				role="presentation"
				cx={sx(n.x)}
				cy={sy(n.y)}
				r={radius(n)}
				class={hover === n.name ? 'fill-accent-2' : 'fill-accent'}
				opacity={dim ? 0.2 : 0.9}
				onmouseenter={() => (hover = n.name)}
				onmouseleave={() => (hover = null)}
			/>
			{#if labeled.has(n.name) || hover === n.name}
				<text
					x={sx(n.x)}
					y={sy(n.y) - radius(n) - 4}
					text-anchor="middle"
					font-size="11"
					class="pointer-events-none fill-ink-2"
					opacity={dim ? 0.25 : 1}
				>{n.name}</text>
			{/if}
		{/each}
	</svg>

	{#if hoverNode}
		<div class="pointer-events-none absolute right-3 top-3 w-64 rounded-lg border border-white/15 bg-page/95 px-4 py-3 shadow-xl">
			<p class="font-semibold text-accent-soft">{hoverNode.name}</p>
			<p class="mt-1 text-xs text-ink-2">
				{hoverNode.messages} messages · gave {hoverNode.reactionsGiven} · received
				{hoverNode.reactionsReceived} reactions · {hoverNode.degree} connections
			</p>
			{#if partners.length}
				<p class="mt-2 text-xs font-medium text-ink-3 uppercase tracking-wide">strongest ties</p>
				<ul class="mt-1 space-y-0.5 text-xs text-ink-2">
					{#each partners as p (p.other)}
						<li>{p.other} <span class="text-ink-3">— {p.weight} interactions</span></li>
					{/each}
				</ul>
			{/if}
		</div>
	{/if}
</div>
<p class="mt-2 text-sm text-ink-3">
	{nodes.length} people ({nodes.length - 57} reacted without ever messaging) · node size = activity ·
	edge weight = reactions + thread replies + @mentions between two people · layout pulls the
	connected together. Hover anyone.
</p>
