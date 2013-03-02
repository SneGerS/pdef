package pdef.provided;

import com.google.common.base.Defaults;
import static com.google.common.base.Preconditions.*;
import com.google.common.primitives.Primitives;
import pdef.*;

import java.util.Map;

class NativeValueDescriptor implements ValueDescriptor {
	private final Class<?> javaClass;
	private final Class<?> primitiveClass;

	NativeValueDescriptor(final Class<?> javaClass) {
		this.javaClass = checkNotNull(javaClass);
		this.primitiveClass = Primitives.unwrap(javaClass);
	}

	@Override
	public Class<?> getJavaClass() { return javaClass; }

	@Override
	public Object getDefaultInstance() { return Defaults.defaultValue(javaClass); }

	@Override
	public SymbolTable<VariableDescriptor> getVariables() { return ImmutableSymbolTable.of(); }

	@Override
	public TypeDescriptor parameterize(final TypeDescriptor... args) {
		throw new UnsupportedOperationException();
	}

	@Override
	public TypeDescriptor bind(Map<VariableDescriptor, TypeDescriptor> argMap) { return this; }
}