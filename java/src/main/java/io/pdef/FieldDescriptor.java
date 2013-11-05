package io.pdef;

public interface FieldDescriptor<M, V> extends FieldAccessor<M, V> {
	/**
	 * Returns a pdef field name.
	 */
	String getName();

	/**
	 * Returns a field type descriptor.
	 */
	DataDescriptor<V> getType();

	/**
	 * Returns whether this field is a discriminator in a message.
	 */
	boolean isDiscriminator();

	/**
	 * Copies a field from a source message to a destination message.
	 */
	void copy(M src, M dst);
}
