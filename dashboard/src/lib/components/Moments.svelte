<script lang="ts">
	import moments from '$lib/data/moments.json';
	import { messages, EVENT_END_MIN, fmtClock } from '$lib/data';
	import { seekReplay } from '$lib/replay.svelte';

	const msgById = new Map(messages.map((m) => [m.id, m]));
	const { bursts, laughLeaders, threadLatency } = moments;
	const maxLaughs = laughLeaders[0].laughs;
</script>

<!-- Burst strip on the shared time axis -->
<div class="relative h-10 rounded-md border border-white/10 bg-surface-2/50">
	{#each bursts as b (b.start)}
		<button
			class="absolute top-0 h-full rounded-sm bg-accent transition-colors hover:bg-accent-2"
			style="left: {(b.start / EVENT_END_MIN) * 100}%; width: {((b.end - b.start) / EVENT_END_MIN) * 100}%; opacity: {0.35 + 0.6 * (b.peakZ / 5)}"
			title="min {b.start}–{b.end}, z = {b.peakZ} — watch this moment"
			aria-label="Watch burst at minute {b.start}"
			onclick={() => seekReplay(b.start)}
		></button>
	{/each}
	{#each [0, 10, 20, 30, 40, 50, 60, 70] as t}
		<span class="absolute -bottom-5 -translate-x-1/2 text-[11px] text-ink-3" style="left: {(t / EVENT_END_MIN) * 100}%">{t}m</span>
	{/each}
</div>
<p class="mt-7 text-sm text-ink-3">
	{bursts.length} moments where the room moved as one — 60-second windows ≥ 1.6 SD above baseline
	activity (messages + reactions).
</p>

<div class="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
	{#each bursts as b (b.start)}
		{@const trigger = b.triggerId ? msgById.get(b.triggerId) : null}
		<button
			class="rounded-xl border border-white/10 bg-surface-2/60 p-4 text-left transition-colors hover:border-accent/50"
			onclick={() => seekReplay(b.start)}
		>
			<p class="text-xs text-ink-3">
				{fmtClock(b.start)}–{fmtClock(b.end)} · z = {b.peakZ} · {b.nMessages} msgs, {b.nReactions} reactions
				· <span class="text-accent-soft">▶ watch</span>
			</p>
			{#if trigger}
				<p class="mt-2 text-sm text-ink">
					<span class="font-medium text-accent-soft">{trigger.name}:</span>
					{trigger.text}
				</p>
			{/if}
		</button>
	{/each}
</div>

<div class="mt-6 grid gap-4 lg:grid-cols-2">
	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="font-semibold text-ink">Who made the room laugh</h3>
		<ol class="mt-4 space-y-2.5">
			{#each laughLeaders as l (l.name)}
				<li class="grid grid-cols-[7rem_1fr_2.5rem] items-center gap-2 text-sm">
					<span class="truncate text-ink-2" title={l.name}>{l.name}</span>
					<div class="h-3.5 overflow-hidden rounded-[4px] bg-white/5">
						<div class="h-full rounded-[4px] bg-accent" style="width: {(l.laughs / maxLaughs) * 100}%"></div>
					</div>
					<span class="text-right text-ink-2" style="font-variant-numeric: tabular-nums">😂{l.laughs}</span>
				</li>
			{/each}
		</ol>
		<p class="mt-3 text-xs text-ink-3">😂 + 🤣 reactions received on their messages</p>
	</div>

	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="font-semibold text-ink">Thread reflexes</h3>
		<div class="mt-4 grid grid-cols-3 gap-3">
			<div>
				<p class="text-2xl font-semibold text-ink">{threadLatency.median_s}s</p>
				<p class="mt-1 text-xs text-ink-3">median reply time</p>
			</div>
			<div>
				<p class="text-2xl font-semibold text-ink">{threadLatency.p25_s}s</p>
				<p class="mt-1 text-xs text-ink-3">fastest quartile</p>
			</div>
			<div>
				<p class="text-2xl font-semibold text-ink">{threadLatency.n}</p>
				<p class="mt-1 text-xs text-ink-3">thread replies</p>
			</div>
		</div>
		<p class="mt-4 text-sm text-ink-2">
			Half of all thread replies landed within {Math.round(threadLatency.median_s)} seconds —
			mid-talk, phones out, nobody pretending otherwise.
		</p>
	</div>
</div>
