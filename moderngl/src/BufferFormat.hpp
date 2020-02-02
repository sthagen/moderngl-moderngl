#pragma once

struct FormatNode {
	int size;
	int count;
	int type;
	bool normalize;
};

struct FormatInfo {
	int size;
	int nodes;
	int divisor;
	bool valid;

	static FormatInfo invalid() {
		FormatInfo invalid;
		invalid.size = 0;
		invalid.nodes = 0;
		invalid.divisor = 0;
		invalid.valid = false;
		return invalid;
	}
};

struct FormatIterator {
	const char * ptr;
	FormatNode node;

	FormatIterator(const char * str);

	FormatInfo info();
	FormatNode * next();
};

extern FormatNode * InvalidFormat;
