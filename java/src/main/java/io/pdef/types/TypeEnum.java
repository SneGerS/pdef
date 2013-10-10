package io.pdef.types;

import java.util.EnumSet;

public enum TypeEnum {
	// Primitives.
	BOOL, INT16, INT32, INT64, FLOAT, DOUBLE, STRING,

	// Collections.
	LIST, SET, MAP,

	// Special types.
	OBJECT, VOID,

	// User-defined types.
	ENUM,
	MESSAGE,
	EXCEPTION,
	INTERFACE;

	private static final EnumSet<TypeEnum> PRIMITIVES;
	private static final EnumSet<TypeEnum> DATA_TYPES;

	static {
		PRIMITIVES = EnumSet.of(BOOL, INT16, INT32, INT64, FLOAT, DOUBLE, STRING);
		DATA_TYPES = EnumSet.copyOf(PRIMITIVES);
		DATA_TYPES.add(OBJECT);
		DATA_TYPES.add(LIST);
		DATA_TYPES.add(SET);
		DATA_TYPES.add(MAP);
		DATA_TYPES.add(ENUM);
		DATA_TYPES.add(MESSAGE);
		DATA_TYPES.add(EXCEPTION);
	}

	public boolean isPrimitive() {
		return PRIMITIVES.contains(this);
	}

	public boolean isDataType() {
		return DATA_TYPES.contains(this);
	}
}