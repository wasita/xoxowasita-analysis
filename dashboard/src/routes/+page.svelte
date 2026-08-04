<script lang="ts">
	import { meta, peakMinute, EVENT_END_MIN, emojiRows } from '$lib/data';
	import Timeline from '$lib/components/Timeline.svelte';
	import Moments from '$lib/components/Moments.svelte';
	import EmojiStreams from '$lib/components/EmojiStreams.svelte';
	import AffectWaves from '$lib/components/AffectWaves.svelte';
	import TopicMap from '$lib/components/TopicMap.svelte';
	import ConnectionGraph from '$lib/components/ConnectionGraph.svelte';
	import AuthorMap from '$lib/components/AuthorMap.svelte';
	import Reconstruction from '$lib/components/Reconstruction.svelte';
	import Leaderboards from '$lib/components/Leaderboards.svelte';
	import Transcript from '$lib/components/Transcript.svelte';

	const stats = [
		{ value: meta.n_messages, label: 'messages' },
		{ value: meta.n_authors, label: 'voices' },
		{ value: meta.n_reactions, label: 'emoji reactions' },
		{ value: `${EVENT_END_MIN} min`, label: 'of defense' },
		{ value: `min ${peakMinute.minute}`, label: `peak — ${peakMinute.messages} msgs` }
	];

	const sections = [
		{ id: 'timeline', title: 'The shape of the defense', kicker: 'messages per minute', component: Timeline },
		{ id: 'moments', title: 'When the room moved as one', kicker: 'burst detection', component: Moments },
		{ id: 'emoji', title: 'The emoji record', kicker: `${emojiRows.length} distinct reactions`, component: EmojiStreams },
		{ id: 'affect', title: 'What the room felt', kicker: 'affect waves', component: AffectWaves },
		{ id: 'topics', title: 'What people talked about', kicker: 'a semantic map', component: TopicMap },
		{ id: 'network', title: 'Who connected with whom', kicker: 'the connection graph', component: ConnectionGraph },
		{ id: 'authors', title: 'Who chats alike', kicker: 'author constellation', component: AuthorMap },
		{ id: 'talk', title: 'The talk, reconstructed from chat alone', kicker: 'the experiment', component: Reconstruction },
		{ id: 'boards', title: 'Leaderboards', kicker: 'the chattiest & most loved', component: Leaderboards },
		{ id: 'transcript', title: 'Every message', kicker: 'the full archive', component: Transcript }
	];
</script>

<header class="mx-auto max-w-4xl px-5 pt-16 pb-10 text-center">
	<h1 class="font-display text-6xl tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-violet-400 via-fuchsia-400 to-pink-400 sm:text-7xl">
		xoxo wasita
	</h1>
	<p class="mt-4 text-lg text-ink-2">
		what 57 people said while Dr. Mahaphanit defended in public
	</p>
	<p class="mt-1 text-sm text-ink-3">
		July 10, 2026 · public dissertation defense ·
		<a href="https://github.com/ljchang/xoxowasita" class="underline decoration-white/30 hover:text-ink-2">the chat app</a>
		Luke built for the audience
	</p>

	<div class="mt-10 grid grid-cols-2 gap-3 sm:grid-cols-5">
		{#each stats as s (s.label)}
			<div class="rounded-xl border border-white/10 bg-surface p-4">
				<p class="text-2xl font-semibold text-ink">{s.value}</p>
				<p class="mt-1 text-xs text-ink-3">{s.label}</p>
			</div>
		{/each}
	</div>

	<nav class="mt-8 flex flex-wrap justify-center gap-x-5 gap-y-1 text-sm text-ink-2">
		{#each sections as s (s.id)}
			<a href="#{s.id}" class="hover:text-accent-soft">{s.title}</a>
		{/each}
	</nav>
</header>

<main class="mx-auto max-w-4xl space-y-20 px-5 pb-24">
	{#each sections as s (s.id)}
		{@const Section = s.component}
		<section id={s.id} class="scroll-mt-8">
			<p class="text-xs font-medium tracking-widest text-accent-soft uppercase">{s.kicker}</p>
			<h2 class="mt-1 mb-6 text-2xl font-semibold text-ink">{s.title}</h2>
			<Section />
		</section>
	{/each}
</main>

<footer class="border-t border-white/10 py-8 text-center text-sm text-ink-3">
	made with 💜 from the
	<a href="https://github.com/ljchang/xoxowasita" class="underline decoration-white/30 hover:text-ink-2">xoxowasita</a>
	chat archive · july 10, 2026
</footer>
