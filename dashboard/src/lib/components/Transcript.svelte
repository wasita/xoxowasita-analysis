<script lang="ts">
	import { messages, topics, fmtClock, type Message } from '$lib/data';

	let query = $state('');
	let topicFilter = $state<string | null>(null);
	let authorFilter = $state<string | null>(null);
	let hoverChip = $state<string | null>(null); // `${msgId}:${emoji}`
	let clearTimer: ReturnType<typeof setTimeout>;
	const chipEnter = (key: string) => {
		clearTimeout(clearTimer);
		hoverChip = key;
	};
	// Only leaving the whole reactions block clears, after a grace period —
	// slipping between chips or off an edge doesn't flicker the names away.
	const blockLeave = () => {
		clearTimer = setTimeout(() => (hoverChip = null), 200);
	};
	const blockEnter = () => clearTimeout(clearTimer);

	// Everyone who participated: message authors plus reaction-only lurkers.
	const messageAuthors = new Set(messages.map((m) => m.name));
	const authors = [
		...new Set([
			...messageAuthors,
			...messages.flatMap((m) => Object.values(m.reactions).flat())
		])
	].sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));

	const reactedTo = (m: Message, name: string) =>
		Object.values(m.reactions).some((users) => users.includes(name));

	// Thread-aware ordering: each parent followed by its replies.
	const parents = messages.filter((m) => !m.parentId);
	const repliesByParent = new Map<string, Message[]>();
	for (const m of messages) {
		if (m.parentId) {
			const list = repliesByParent.get(m.parentId) ?? [];
			list.push(m);
			repliesByParent.set(m.parentId, list);
		}
	}
	const ordered = parents.flatMap((p) => [p, ...(repliesByParent.get(p.id) ?? [])]);

	const matches = (m: Message) => {
		if (topicFilter && m.topic !== topicFilter) return false;
		if (authorFilter) {
			// Lurkers who never messaged: show what they reacted to instead.
			const ok = messageAuthors.has(authorFilter)
				? m.name === authorFilter
				: reactedTo(m, authorFilter);
			if (!ok) return false;
		}
		const q = query.trim().toLowerCase();
		return !q || m.text.toLowerCase().includes(q) || m.name.toLowerCase().includes(q);
	};
	const visible = $derived(ordered.filter(matches));
</script>

<div class="mb-4 flex flex-wrap items-center gap-3">
	<input
		type="search"
		placeholder="search text or name…"
		bind:value={query}
		class="w-64 rounded-lg border border-white/15 bg-surface-2 px-3 py-1.5 text-sm text-ink
		       placeholder:text-ink-3 focus:border-accent focus:outline-none"
	/>
	<select
		bind:value={topicFilter}
		class="rounded-lg border border-white/15 bg-surface-2 px-2 py-1.5 text-sm text-ink-2 focus:border-accent focus:outline-none"
	>
		<option value={null}>every topic</option>
		{#each Object.entries(topics) as [key, t] (key)}
			<option value={key}>{t.label}</option>
		{/each}
	</select>
	<select
		bind:value={authorFilter}
		class="rounded-lg border border-white/15 bg-surface-2 px-2 py-1.5 text-sm text-ink-2 focus:border-accent focus:outline-none"
	>
		<option value={null}>everyone</option>
		{#each authors as a (a)}
			<option value={a}>{a}</option>
		{/each}
	</select>
	<span class="text-sm text-ink-3">
		{visible.length} of {messages.length} messages{#if authorFilter && !messageAuthors.has(authorFilter)}
			· {authorFilter} never messaged — showing what they reacted to{/if}
	</span>
</div>

<div class="max-h-[36rem] space-y-1.5 overflow-y-auto rounded-xl border border-white/10 bg-surface-2/40 p-4">
	{#each visible as m (m.id)}
		<div class="rounded-lg px-3 py-2 hover:bg-white/5 {m.parentId ? 'ml-8 border-l-2 border-accent/30' : ''}">
			<p class="text-xs text-ink-3">
				<span class="font-medium text-accent-soft">{m.name}</span>
				· {fmtClock(m.minutes)}
				· <span class="text-ink-3">{topics[m.topic].label}</span>
			</p>
			<p class="mt-0.5 text-[15px] text-ink whitespace-pre-wrap">{m.text}</p>
			{#if Object.keys(m.reactions).length}
				<div role="presentation" onmouseenter={blockEnter} onmouseleave={blockLeave}>
					<p class="mt-1 flex flex-wrap gap-1.5">
						{#each Object.entries(m.reactions) as [emoji, users] (emoji)}
							{@const key = `${m.id}:${emoji}`}
							<span
								role="presentation"
								class="rounded-full border border-white/10 bg-white/5 px-2 py-1 text-xs text-ink-2 transition-colors
								       {hoverChip === key ? 'border-accent/50 text-ink' : ''}"
								onmouseenter={() => chipEnter(key)}
							>
								{emoji} {users.length}
							</span>
						{/each}
					</p>
					{#each Object.entries(m.reactions) as [emoji, users] (emoji)}
						{#if hoverChip === `${m.id}:${emoji}`}
							<p class="mt-1 text-xs text-ink-3">{emoji} {users.join(', ')}</p>
						{/if}
					{/each}
				</div>
			{/if}
		</div>
	{:else}
		<p class="p-4 text-sm text-ink-3">nothing matches — try fewer letters</p>
	{/each}
</div>
