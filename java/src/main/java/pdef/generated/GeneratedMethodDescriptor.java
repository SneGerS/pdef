package pdef.generated;

import static com.google.common.base.Preconditions.*;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.Lists;
import pdef.MethodDescriptor;
import pdef.TypeDescriptor;
import pdef.VariableDescriptor;

import java.util.List;
import java.util.Map;

public abstract class GeneratedMethodDescriptor implements MethodDescriptor {
	private final String name;
	private final List<TypeDescriptor> args;

	public GeneratedMethodDescriptor(final String name, final TypeDescriptor... args) {
		this.name = checkNotNull(name);
		this.args = ImmutableList.copyOf(args);
	}

	@Override
	public String getName() {
		return name;
	}

	@Override
	public List<TypeDescriptor> getArgs() {
		return args;
	}

	@Override
	public MethodDescriptor bind(final Map<VariableDescriptor, TypeDescriptor> argMap) {
		List<TypeDescriptor> parameterized = Lists.newArrayList();
		for (TypeDescriptor arg : args) {
			TypeDescriptor barg = arg.bind(argMap);
			parameterized.add(barg);
		}
		if (parameterized.equals(args)) return this;
		return new ParameterizedMethodDescriptor(this, args);
	}

}
