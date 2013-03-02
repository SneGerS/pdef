package pdef.fixtures;

import pdef.EnumDescriptor;
import pdef.EnumType;
import pdef.generated.GeneratedEnumDescriptor;

public enum Type implements EnumType {
	ENTITY, IMAGE, USER;

	@Override
	public EnumDescriptor getDescriptor() {
		return descriptor;
	}

	private static final EnumDescriptor descriptor = new GeneratedEnumDescriptor(Type.class);
	public static EnumDescriptor getDescriptorForType() {
		return descriptor;
	}
}
