package pdef.fixtures;

import pdef.ImmutableSymbolTable;
import pdef.Message;
import pdef.SymbolTable;
import pdef.descriptors.AbstractFieldDescriptor;
import pdef.descriptors.AbstractMessageDescriptor;
import pdef.descriptors.FieldDescriptor;
import pdef.descriptors.MessageDescriptor;

public class User extends Entity {
	private Image image;

	public Image getImage() {
		return image;
	}

	public User setImage(final Image image) {
		this.image = image;
		return this;
	}

	@Override
	public MessageDescriptor getDescriptor() {
		return Descriptor.getInstance();
	}

	public static class Descriptor extends AbstractMessageDescriptor {
		private static final Descriptor INSTANCE = new Descriptor();
		public static Descriptor getInstance() {
			INSTANCE.link();
			return INSTANCE;
		}

		private MessageDescriptor base;
		private SymbolTable<FieldDescriptor> declaredFields;
		private SymbolTable<FieldDescriptor> fields;

		private Descriptor() {
			super(User.class);
		}

		@Override
		public MessageDescriptor getBase() {
			return base;
		}

		@Override
		public SymbolTable<FieldDescriptor> getDeclaredFields() {
			return declaredFields;
		}

		@Override
		public SymbolTable<FieldDescriptor> getFields() {
			return fields;
		}

		@Override
		protected void doLink() {
			base = Entity.Descriptor.getInstance();
			declaredFields = ImmutableSymbolTable.<FieldDescriptor>of(
					new AbstractFieldDescriptor("avatar", Image.Descriptor.getInstance()) {
						@Override
						public Object get(final Message message) {
							return ((User) message).getImage();
						}

						@Override
						public void set(final Message message, final Object value) {
							((User) message).setImage((Image) value);
						}
					}
			);
			fields = base.getFields().merge(declaredFields);
		}
	}
}
