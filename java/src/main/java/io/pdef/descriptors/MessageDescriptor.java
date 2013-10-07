package io.pdef.descriptors;

import com.google.common.base.Supplier;
import com.google.common.collect.ImmutableList;
import com.google.common.collect.Lists;
import com.google.common.collect.Maps;
import io.pdef.Message;
import io.pdef.TypeEnum;

import javax.annotation.Nullable;
import java.util.List;
import java.util.Map;

import static com.google.common.base.Preconditions.checkNotNull;

public class MessageDescriptor extends DataDescriptor {
	private final Class<?> javaClass;
	private final MessageDescriptor base;
	private final boolean form;

	private final Enum<?> discriminatorValue;
	private final FieldDescriptor discriminator;
	private final List<Supplier<MessageDescriptor>> subtypes;

	private final List<FieldDescriptor> declaredFields;
	private final List<FieldDescriptor> fields;

	private final Supplier<? extends Message.Builder> builder;

	public static Builder builder() {
		return new Builder();
	}

	private MessageDescriptor(final Builder b) {
		super(TypeEnum.MESSAGE);
		javaClass = checkNotNull(b.javaClass);
		base = b.base;
		discriminatorValue = b.discriminatorValue;
		subtypes = ImmutableList.copyOf(b.subtypes);

		declaredFields = buildDeclaredFields(b.declaredFields, this);
		fields = buildFields(declaredFields, base);
		discriminator = getDiscriminator(fields);

		builder = checkNotNull(b.builder);
		form = b.form;
	}

	public Class<?> getJavaClass() {
		return javaClass;
	}

	public MessageDescriptor getBase() {
		return base;
	}

	public boolean isForm() {
		return form;
	}

	public Enum<?> getDiscriminatorValue() {
		return discriminatorValue;
	}

	public List<FieldDescriptor> getDeclaredFields() {
		return declaredFields;
	}

	public List<FieldDescriptor> getInheritedFields() {
		return base != null ? base.getFields() : ImmutableList.<FieldDescriptor>of();
	}

	public List<Supplier<MessageDescriptor>> getSubtypes() {
		return subtypes;
	}

	@Nullable
	public MessageDescriptor getSubtype(final Enum<?> value) {
		if (value == null) {
			return null;
		}

		for (Supplier<MessageDescriptor> supplier : subtypes) {
			MessageDescriptor subtype = supplier.get();
			if (value.equals(subtype.getDiscriminatorValue())) {
				return subtype;
			}
		}

		return null;
	}

	public List<FieldDescriptor> getFields() {
		return fields;
	}

	public FieldDescriptor getDiscriminator() {
		return discriminator;
	}

	public Message.Builder createBuilder() {
		return builder.get();
	}

	public Message.Builder toBuilder(final Message message) {
		if (message == null) return null;
		return createBuilder().merge(message);
	}

	@Override
	public Map<String, Object> toObject(final Object o) {
		if (o == null) return null;
		Message message = (Message) o;

		Map<String, Object> map = Maps.newLinkedHashMap();
		for (FieldDescriptor field : fields) {
			Object value = field.get(message);
			Object serialized = field.getType().toObject(value);
			if (serialized == null) {
				continue;
			}

			map.put(field.getName(), serialized);
		}

		return map;
	}

	@Override
	public Message parseObject(final Object o) {
		if (o == null) return null;
		Map<?, ?> map = (Map<?, ?>) o;

		if (discriminator != null) {
			Object dvalue = map.get(discriminator.getName());
			Enum<?> denum = (Enum<?>) discriminator.getType().parseObject(dvalue);

			MessageDescriptor subtype = getSubtype(denum);
			if (subtype != null && subtype != this) {
				return subtype.parseObject(o);
			}
		}

		Message.Builder builder = createBuilder();
		for (FieldDescriptor field : getFields()) {
			Object value = map.get(field.getName());
			Object parsed = field.getType().parseObject(value);
			if (parsed == null) {
				continue;
			}

			field.set(builder, parsed);
		}

		return builder.build();
	}

	public static class Builder {
		private Class<?> javaClass;
		private MessageDescriptor base;
		private Enum<?> discriminatorValue;
		private Supplier<? extends Message.Builder> builder;
		private final List<FieldDescriptor.Builder> declaredFields;
		private final List<Supplier<MessageDescriptor>> subtypes;
		private boolean form;

		private Builder() {
			declaredFields = Lists.newArrayList();
			subtypes = Lists.newArrayList();
		}

		public Builder setJavaClass(final Class<?> cls) {
			this.javaClass = cls;
			return this;
		}

		public Builder setBase(final MessageDescriptor base) {
			this.base = base;
			return this;
		}

		public Builder setForm(final boolean form) {
			this.form = form;
			return this;
		}

		public Builder setDiscriminatorValue(final Enum<?> value) {
			this.discriminatorValue = value;
			return this;
		}

		public Builder setBuilder(final Supplier<? extends Message.Builder> builder) {
			this.builder = builder;
			return this;
		}

		public Builder addField(final FieldDescriptor.Builder field) {
			declaredFields.add(field);
			return this;
		}

		public Builder addSubtype(final Supplier<MessageDescriptor> subtype) {
			subtypes.add(subtype);
			return this;
		}

		public MessageDescriptor build() {
			return new MessageDescriptor(this);
		}
	}

	private static ImmutableList<FieldDescriptor> buildDeclaredFields(
			final Iterable<FieldDescriptor.Builder> fields, final MessageDescriptor message) {
		ImmutableList.Builder<FieldDescriptor> temp = ImmutableList.builder();
		for (FieldDescriptor.Builder fb : fields) {
			FieldDescriptor field = fb.build(message);
			temp.add(field);
		}
		return temp.build();
	}

	private static ImmutableList<FieldDescriptor> buildFields(
			final Iterable<FieldDescriptor> declaredFields, final MessageDescriptor base) {
		return ImmutableList.<FieldDescriptor>builder()
				.addAll(base == null ? ImmutableList.<FieldDescriptor>of() : base.getFields())
				.addAll(declaredFields)
				.build();
	}

	private static FieldDescriptor getDiscriminator(final Iterable<FieldDescriptor> fields) {
		for (FieldDescriptor field : fields) {
			if (field.isDiscriminator()) {
				return field;
			}
		}
		return null;
	}
}