#include "BufferFormat.hpp"

#include "OpenGL.hpp"

FormatNode * InvalidFormat = (FormatNode *)(-1);

FormatIterator::FormatIterator(const char * str) : ptr(str) {
}

FormatInfo FormatIterator::info() {
	FormatInfo info;
	info.size = 0;
	info.nodes = 0;
	info.divisor = 0;
	info.valid = true;

	FormatIterator it = FormatIterator(ptr);
	while (FormatNode * node = it.next()) {
		if (node == InvalidFormat) {
			return FormatInfo::invalid();
		}
		info.size += node->size;
		if (node->type) {
			++info.nodes;
		}
	}

	char post_chr = *it.ptr++;

	if (post_chr == '/') {
		char per_type = *it.ptr++;

		switch (per_type) {
			case 'i':
				info.divisor = 1;
				break;

			case 'r':
				info.divisor = 0x7fffffff;
				break;

			case 'v':
				break;

			default:
				return FormatInfo::invalid();
		}

		if (*it.ptr) {
			return FormatInfo::invalid();
		}
	}

	return info;
}

FormatNode * FormatIterator::next() {
	node.count = 0;
	while (true) {
		char chr = *ptr++;
		switch (chr) {
			case '0':
			case '1':
			case '2':
			case '3':
			case '4':
			case '5':
			case '6':
			case '7':
			case '8':
			case '9':
				node.count = node.count * 10 + chr - '0';
				break;

			case 'f':
				if (node.count == 0) {
					node.count = 1;
				}
				switch (*ptr++) {
					case '1':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 1 * node.count;
						node.type = GL_UNSIGNED_BYTE;
						node.normalize = true;
						break;
					case '2':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 2 * node.count;
						node.type = GL_HALF_FLOAT;
						node.normalize = false;
						break;
					case '4':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 4 * node.count;
						node.type = GL_FLOAT;
						node.normalize = false;
						break;
					case '8':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 8 * node.count;
						node.type = GL_DOUBLE;
						node.normalize = false;
						break;
					case 0:
					case '/':
						--ptr;
					case ' ':
						node.size = 4 * node.count;
						node.type = GL_FLOAT;
						node.normalize = false;
						break;
					default:
						return InvalidFormat;
				}
				return &node;

			case 'i':
				if (node.count == 0) {
					node.count = 1;
				}
				node.normalize = false;
				switch (*ptr++) {
					case '1':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 1 * node.count;
						node.type = GL_BYTE;
						break;
					case '2':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 2 * node.count;
						node.type = GL_SHORT;
						break;
					case '4':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 4 * node.count;
						node.type = GL_INT;
						break;
					case 0:
					case '/':
						--ptr;
					case ' ':
						node.size = 4 * node.count;
						node.type = GL_INT;
						break;
					default:
						return InvalidFormat;
				}
				return &node;

			case 'u':
				if (node.count == 0) {
					node.count = 1;
				}
				node.normalize = false;
				switch (*ptr++) {
					case '1':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 1 * node.count;
						node.type = GL_UNSIGNED_BYTE;
						break;
					case '2':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 2 * node.count;
						node.type = GL_UNSIGNED_SHORT;
						break;
					case '4':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 4 * node.count;
						node.type = GL_UNSIGNED_INT;
						break;
					case 0:
					case '/':
						--ptr;
					case ' ':
						node.size = 4 * node.count;
						node.type = GL_UNSIGNED_INT;
						break;
					default:
						return InvalidFormat;
				}
				return &node;

			case 'x':
				if (node.count == 0) {
					node.count = 1;
				}
				node.type = 0;
				node.normalize = false;
				switch (*ptr++) {
					case '1':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 1 * node.count;
						break;
					case '2':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 2 * node.count;
						break;
					case '4':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 4 * node.count;
						break;
					case '8':
						if (*ptr && *ptr != ' ' && *ptr != '/') {
							return InvalidFormat;
						}
						node.size = 8 * node.count;
						break;
					case 0:
					case '/':
						--ptr;
					case ' ':
						node.size = 1 * node.count;
						break;
					default:
						return InvalidFormat;
				}
				return &node;

			case ' ':
				break;

			case 0:
			case '/':
				--ptr;
				return node.count ? InvalidFormat : 0;

			default:
				return InvalidFormat;
		}
	}
}
