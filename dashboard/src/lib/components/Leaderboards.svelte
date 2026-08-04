<script lang="ts">
	import { topSenders, topReactors, mostReacted, biggestThreads, reactionCount } from '$lib/data';

	const N = 8;
	const senders = topSenders.slice(0, N);
	const reactors = topReactors.slice(0, N);
	const maxSent = senders[0][1];
	const maxGiven = reactors[0][1];

	const topEmoji = (m: (typeof mostReacted)[number]) =>
		Object.entries(m.reactions)
			.sort((a, b) => b[1].length - a[1].length)
			.slice(0, 3)
			.map(([e, users]) => `${e}${users.length}`)
			.join(' ');
</script>

{#snippet barList(title: string, rows: [string, number][], max: number, unit: string)}
	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="font-semibold text-ink">{title}</h3>
		<ol class="mt-4 space-y-2.5">
			{#each rows as [name, count] (name)}
				<li class="grid grid-cols-[7rem_1fr_2rem] items-center gap-2 text-sm">
					<span class="truncate text-ink-2" title={name}>{name}</span>
					<div class="h-3.5 overflow-hidden rounded-[4px] bg-white/5">
						<div class="h-full rounded-[4px] bg-accent" style="width: {(count / max) * 100}%"></div>
					</div>
					<span class="text-right text-ink-2" style="font-variant-numeric: tabular-nums">{count}</span>
				</li>
			{/each}
		</ol>
		<p class="mt-3 text-xs text-ink-3">{unit}</p>
	</div>
{/snippet}

<div class="grid gap-4 lg:grid-cols-2">
	{@render barList('Most messages', senders, maxSent, 'messages sent')}
	{@render barList('Most reactions given', reactors, maxGiven, 'emoji taps handed out')}

	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="font-semibold text-ink">Most-reacted messages</h3>
		<ol class="mt-4 space-y-3">
			{#each mostReacted.slice(0, 5) as m (m.id)}
				<li class="text-sm">
					<p class="text-ink-2">
						<span class="font-medium text-accent-soft">{m.name}</span>
						<span class="text-ink-3"> · min {Math.round(m.minutes)}</span>
					</p>
					<p class="mt-0.5 text-ink">{m.text}</p>
					<p class="mt-0.5 text-ink-3">{topEmoji(m)} · {reactionCount(m)} total</p>
				</li>
			{/each}
		</ol>
	</div>

	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="font-semibold text-ink">Biggest threads</h3>
		<ol class="mt-4 space-y-3">
			{#each biggestThreads.slice(0, 5) as m (m.id)}
				<li class="text-sm">
					<p class="text-ink-2">
						<span class="font-medium text-accent-soft">{m.name}</span>
						<span class="text-ink-3"> · min {Math.round(m.minutes)}</span>
					</p>
					<p class="mt-0.5 text-ink">{m.text}</p>
					<p class="mt-0.5 text-ink-3">{m.replyCount} replies</p>
				</li>
			{/each}
		</ol>
	</div>
</div>
