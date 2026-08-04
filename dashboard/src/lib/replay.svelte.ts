/** Cross-component control for the video replay: seek requests in chat-minutes. */
export const replayControl = $state<{ request: number | null }>({ request: null });

export function seekReplay(chatMinutes: number) {
	replayControl.request = chatMinutes;
	document.getElementById('replay')?.scrollIntoView({ behavior: 'smooth' });
}
