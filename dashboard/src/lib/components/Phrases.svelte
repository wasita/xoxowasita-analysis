<script lang="ts">
	import phrasesData from '$lib/data/phrases.json';
	import { EVENT_END_MIN } from '$lib/data';

	const phrases = phrasesData.phrases;
</script>

<div class="grid gap-3 sm:grid-cols-2">
	{#each phrases as p (p.phrase)}
		<div class="rounded-xl border border-white/10 bg-surface-2/60 p-4">
			<p class="text-[15px] font-medium text-ink">“{p.phrase}”</p>
			<p class="mt-1 text-xs text-ink-3">
				coined by <span class="text-accent-soft">{p.coiner}</span> at min {Math.round(p.firstMinute)}
				· said ×{p.count} by {p.authors} people
			</p>
			<div class="relative mt-2 h-4 rounded bg-white/5">
				{#each p.occurrences as min, i (i)}
					<div
						class="absolute top-1/2 size-2 -translate-y-1/2 rounded-full {i === 0 ? 'bg-accent-2' : 'bg-accent'}"
						style="left: calc({(min / EVENT_END_MIN) * 100}% - 4px)"
						title="min {Math.round(min)}"
					></div>
				{/each}
			</div>
		</div>
	{/each}
</div>
<p class="mt-3 text-sm text-ink-3">
	Phrases used at least 3 times by at least 2 different people. Pink dot = first use; violet
	dots = the echoes, across the {EVENT_END_MIN} minutes.
</p>
