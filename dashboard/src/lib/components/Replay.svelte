<script lang="ts">
	import { browser } from '$app/environment';
	import { messages, segments, fmtClock, type Message } from '$lib/data';
	import { replayControl } from '$lib/replay.svelte';

	const VIDEO_URL =
		'https://github.com/wasita/xoxowasita-analysis/releases/download/recording/defense.mp4';

	/** Video time (s) at which the first chat message was sent. */
	const DEFAULT_OFFSET = 0;

	let offset = $state(DEFAULT_OFFSET);
	let currentTime = $state(0);
	let videoOk = $state(true);
	let videoEl = $state<HTMLVideoElement | null>(null);
	let chatEl = $state<HTMLDivElement | null>(null);
	let pinned = $state(true); // autoscroll unless the user scrolls up

	if (browser) {
		const saved = localStorage.getItem('replayOffset');
		if (saved !== null) offset = Number(saved);
	}
	const setOffset = (v: number) => {
		offset = Math.round(v * 10) / 10;
		if (browser) localStorage.setItem('replayOffset', String(offset));
	};

	const chatSeconds = $derived(currentTime - offset);
	const visible = $derived(messages.filter((m) => m.minutes * 60 <= chatSeconds));
	const currentSegment = $derived(
		segments.find((s) => chatSeconds / 60 >= s.start && chatSeconds / 60 < s.end)
	);

	$effect(() => {
		visible.length; // track
		if (pinned && chatEl) chatEl.scrollTop = chatEl.scrollHeight;
	});

	// External seek requests (e.g. clicking a burst) arrive in chat-minutes.
	$effect(() => {
		if (replayControl.request !== null && videoEl) {
			videoEl.currentTime = replayControl.request * 60 + offset;
			videoEl.play();
			replayControl.request = null;
		}
	});

	const onChatScroll = () => {
		if (!chatEl) return;
		pinned = chatEl.scrollHeight - chatEl.scrollTop - chatEl.clientHeight < 60;
	};

	const seekToSegment = (startMin: number) => {
		if (videoEl) videoEl.currentTime = startMin * 60 + offset;
	};

	const reactionSummary = (m: Message) =>
		Object.entries(m.reactions)
			.sort((a, b) => b[1].length - a[1].length)
			.map(([e, users]) => `${e}${users.length > 1 ? users.length : ''}`)
			.join(' ');
</script>

{#if videoOk}
	<div class="grid gap-4 lg:grid-cols-[3fr_2fr]">
		<div>
			<!-- svelte-ignore a11y_media_has_caption -->
			<video
				bind:this={videoEl}
				src={VIDEO_URL}
				controls
				preload="metadata"
				class="w-full rounded-xl border border-white/10 bg-black"
				ontimeupdate={() => (currentTime = videoEl?.currentTime ?? 0)}
				onerror={() => (videoOk = false)}
			></video>

			<div class="mt-3 flex flex-wrap items-center gap-2 text-sm text-ink-2">
				<span class="text-ink-3">sync:</span>
				<button class="rounded border border-white/15 px-2 py-0.5 hover:border-accent" onclick={() => setOffset(offset - 1)}>−1s</button>
				<input
					type="number"
					step="0.5"
					value={offset}
					onchange={(e) => setOffset(Number(e.currentTarget.value))}
					class="w-20 rounded border border-white/15 bg-surface-2 px-2 py-0.5 text-ink"
				/>
				<button class="rounded border border-white/15 px-2 py-0.5 hover:border-accent" onclick={() => setOffset(offset + 1)}>+1s</button>
				<button
					class="rounded border border-accent/50 bg-accent/15 px-2 py-0.5 hover:bg-accent/30"
					onclick={() => setOffset(currentTime)}
				>
					first message lands here
				</button>
			</div>
			<p class="mt-1 text-xs text-ink-3">
				offset = video seconds at chat's first message ("hi!" — during Luke's app reveal).
				Scrub to that moment, hit the button once; it sticks in your browser.
			</p>

			{#if currentSegment}
				<p class="mt-3 rounded-lg border border-white/10 bg-surface-2/60 px-3 py-2 text-sm text-ink-2">
					<span class="text-accent-soft font-medium">now:</span>
					{currentSegment.title}
				</p>
			{/if}
		</div>

		<div class="flex h-[28rem] flex-col rounded-xl border border-white/10 bg-surface-2/40 lg:h-auto lg:max-h-[34rem]">
			<p class="border-b border-white/10 px-4 py-2 text-xs font-medium tracking-wide text-ink-3 uppercase">
				live chat · {visible.length} messages · {fmtClock(Math.max(chatSeconds, 0) / 60)}
			</p>
			<div bind:this={chatEl} onscroll={onChatScroll} class="flex-1 space-y-1.5 overflow-y-auto p-3">
				{#each visible as m (m.id)}
					<div class="rounded-lg bg-white/5 px-3 py-1.5 {m.parentId ? 'ml-6 border-l-2 border-accent/30' : ''}">
						<p class="text-xs">
							<span class="font-medium text-accent-soft">{m.name}</span>
							<span class="text-ink-3"> {fmtClock(m.minutes)}</span>
						</p>
						<p class="text-sm text-ink whitespace-pre-wrap">{m.text}</p>
						{#if Object.keys(m.reactions).length}
							<p class="mt-0.5 text-xs text-ink-2">{reactionSummary(m)}</p>
						{/if}
					</div>
				{:else}
					<p class="p-3 text-sm text-ink-3">press play — chat starts with the app reveal</p>
				{/each}
			</div>
			{#if !pinned}
				<button
					class="border-t border-white/10 py-1.5 text-xs text-accent-soft hover:bg-white/5"
					onclick={() => { pinned = true; if (chatEl) chatEl.scrollTop = chatEl.scrollHeight; }}
				>
					↓ back to live
				</button>
			{/if}
		</div>
	</div>
{:else}
	<div class="rounded-xl border border-white/10 bg-surface-2/60 p-6 text-sm text-ink-2">
		Recording not available yet — the chat replay will appear here once the video is uploaded.
	</div>
{/if}
