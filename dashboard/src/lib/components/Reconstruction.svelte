<script lang="ts">
	import { segments, verdict } from '$lib/data';
</script>

<ol class="relative ml-3 border-l border-white/10">
	{#each segments as seg, i (seg.start)}
		<li id="segment-{i}" class="relative mb-8 pl-6 last:mb-0 scroll-mt-24">
			<span
				class="absolute -left-[5px] top-1.5 size-2.5 rounded-full
				       {seg.confidence === 'verified' ? 'bg-accent' : 'bg-accent/40 ring-1 ring-accent/60'}"
			></span>
			<p class="text-xs font-medium tracking-wide text-ink-3 uppercase">
				min {Math.round(seg.start)}–{Math.round(seg.end)} · {seg.confidence}
			</p>
			<h3 class="mt-1 text-lg font-semibold text-ink">{seg.title}</h3>
			<p class="mt-1.5 text-[15px] leading-relaxed text-ink-2">{seg.inference}</p>
			<p class="mt-1.5 text-sm text-ink-3"><span class="font-medium">Evidence:</span> {seg.evidence}</p>
		</li>
	{/each}
</ol>

<div class="mt-10 grid gap-4 sm:grid-cols-2">
	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="font-semibold text-accent-soft">What the chat preserved</h3>
		<ul class="mt-3 space-y-2 text-sm text-ink-2">
			{#each verdict.recoverable as item}
				<li class="flex gap-2"><span class="text-accent-soft">✓</span><span>{item}</span></li>
			{/each}
		</ul>
	</div>
	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-5">
		<h3 class="font-semibold text-accent-2">What only the recording knew</h3>
		<ul class="mt-3 space-y-2 text-sm text-ink-2">
			{#each verdict.lost as item}
				<li class="flex gap-2"><span class="text-accent-2">✗</span><span>{item}</span></li>
			{/each}
		</ul>
	</div>
</div>

<blockquote class="mt-6 rounded-xl border border-accent/30 bg-accent/10 p-5 text-[15px] leading-relaxed text-ink">
	{verdict.punchline}
</blockquote>
