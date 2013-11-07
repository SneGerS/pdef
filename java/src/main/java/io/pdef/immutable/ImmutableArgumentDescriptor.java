package io.pdef.immutable;

import io.pdef.ArgumentDescriptor;
import io.pdef.DataTypeDescriptor;

/**
 * ArgumentDescriptor provides a method argument name and type.
 * @param <V> Argument class.
 */
public class ImmutableArgumentDescriptor<V> implements ArgumentDescriptor<V> {
	private final String name;
	private final DataTypeDescriptor<V> type;

	public static <V> ArgumentDescriptor<V> of(final String name,
			final DataTypeDescriptor<V> type) {
		return new ImmutableArgumentDescriptor<V>(name, type);
	}

	public ImmutableArgumentDescriptor(final String name, final DataTypeDescriptor<V> type) {
		if (name == null) throw new NullPointerException("name");
		if (type == null) throw new NullPointerException("type");

		this.name = name;
		this.type = type;
	}

	@Override
	public String toString() {
		return "ArgumentDescriptor{'" + name + '\'' + ", " + type + '}';
	}

	@Override
	public String getName() {
		return name;
	}

	@Override
	public DataTypeDescriptor<V> getType() {
		return type;
	}
}
