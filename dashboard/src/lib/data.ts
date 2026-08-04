import chat from './data/chat.json';
import topicsRaw from './data/topics.json';
import segmentsRaw from './data/segments.json';

export interface Message {
	id: string;
	name: string;
	text: string;
	ts: number;
	minutes: number;
	parentId: string | null;
	replyCount: number;
	reactions: Record<string, string[]>; // emoji -> reactor names
	topic: string;
}

export interface Segment {
	start: number;
	end: number;
	title: string;
	inference: string;
	evidence: string;
	confidence: string;
}

export interface TopicInfo {
	label: string;
	color: string;
}

const topicById = new Map(topicsRaw.points.map((p) => [p.id, p]));

/** All messages, chronological, topic attached. */
export const messages: Message[] = chat.messages.map((m) => ({
	...m,
	reactions: m.reactions as Record<string, string[]>,
	topic: topicById.get(m.id)?.topic ?? 'meta'
}));

export const topics: Record<string, TopicInfo> = topicsRaw.topics;
export const points = topicsRaw.points;
export const segments: Segment[] = segmentsRaw.segments;
export const verdict = segmentsRaw.verdict;
export const meta = chat.meta;

/** The live event window — one straggler message arrived 21 h later. */
export const EVENT_END_MIN = 72;
export const eventMessages = messages.filter((m) => m.minutes <= EVENT_END_MIN);

export const reactionCount = (m: Message) =>
	Object.values(m.reactions).reduce((n, users) => n + users.length, 0);

// --- timeline ---------------------------------------------------------------

export interface MinuteBin {
	minute: number;
	messages: number;
	reactions: number;
}

export const perMinute: MinuteBin[] = (() => {
	const bins: MinuteBin[] = Array.from({ length: EVENT_END_MIN }, (_, i) => ({
		minute: i,
		messages: 0,
		reactions: 0
	}));
	for (const m of eventMessages) {
		const b = bins[Math.min(Math.floor(m.minutes), EVENT_END_MIN - 1)];
		b.messages += 1;
		b.reactions += reactionCount(m); // reactions carry no ts; message ts is the proxy
	}
	return bins;
})();

export const peakMinute = perMinute.reduce((a, b) => (b.messages > a.messages ? b : a));

// --- emoji ------------------------------------------------------------------

export interface EmojiRow {
	emoji: string;
	total: number;
	/** counts per 2-minute bin across the event */
	bins: number[];
}

export const EMOJI_BIN_MIN = 2;
const nEmojiBins = Math.ceil(EVENT_END_MIN / EMOJI_BIN_MIN);

export const emojiRows: EmojiRow[] = (() => {
	const rows = new Map<string, EmojiRow>();
	for (const m of eventMessages) {
		for (const [emoji, users] of Object.entries(m.reactions)) {
			let row = rows.get(emoji);
			if (!row) {
				row = { emoji, total: 0, bins: Array(nEmojiBins).fill(0) };
				rows.set(emoji, row);
			}
			row.total += users.length;
			row.bins[Math.min(Math.floor(m.minutes / EMOJI_BIN_MIN), nEmojiBins - 1)] += users.length;
		}
	}
	return [...rows.values()].sort((a, b) => b.total - a.total);
})();

// --- leaderboards -----------------------------------------------------------

const tally = (entries: Iterable<string>) => {
	const counts = new Map<string, number>();
	for (const k of entries) counts.set(k, (counts.get(k) ?? 0) + 1);
	return [...counts.entries()].sort((a, b) => b[1] - a[1]);
};

export const topSenders = tally(messages.map((m) => m.name));

export const topReactors = tally(
	messages.flatMap((m) => Object.values(m.reactions).flat())
);

export const mostReacted = [...messages].sort((a, b) => reactionCount(b) - reactionCount(a));

export const biggestThreads = messages
	.filter((m) => m.replyCount > 0)
	.sort((a, b) => b.replyCount - a.replyCount);

export const fmtClock = (minutes: number) => {
	const mm = Math.floor(minutes);
	const ss = Math.round((minutes - mm) * 60);
	return `${mm}:${String(ss).padStart(2, '0')}`;
};
