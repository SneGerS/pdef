package io.pdef.descriptors;

import com.google.common.base.Objects;
import com.google.common.base.Throwables;
import com.google.common.collect.ImmutableList;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Type;
import java.util.List;

import static com.google.common.base.Preconditions.checkNotNull;

public class MethodDescriptor {
	private final Method method;
	private final String name;
	private final Type resultType;
	private final Descriptor result;
	private final List<Descriptor> args;
	private final List<Type> argTypes;

	public MethodDescriptor(final Method method, final DescriptorPool pool) {
		this.method = checkNotNull(method);
		name = method.getName();
		resultType = method.getGenericReturnType();
		result = pool.getDescriptor(resultType);
		argTypes = ImmutableList.copyOf(method.getGenericParameterTypes());

		ImmutableList.Builder<Descriptor> builder = ImmutableList.builder();
		for (Type type : argTypes) {
			Descriptor arg = pool.getDescriptor(type);
			builder.add(arg);
		}
		args = builder.build();
	}

	@Override
	public String toString() {
		return Objects.toStringHelper(this)
				.addValue(name)
				.toString();
	}

	public Method getMethod() {
		return method;
	}

	public String getName() {
		return name;
	}

	public Descriptor getResult() {
		return result;
	}

	public Type getResultType() {
		return resultType;
	}

	public List<Descriptor> getArgs() {
		return args;
	}

	public List<Type> getArgTypes() {
		return argTypes;
	}

	public Object invoke(final Object object, final List<?> args) {
		Object[] array = args.toArray();
		try {
			return method.invoke(object, array);
		} catch (IllegalAccessException e) {
			throw new RuntimeException(e);
		} catch (InvocationTargetException e) {
			Throwable cause = e.getCause();
			throw Throwables.propagate(cause);
		}
	}
}
