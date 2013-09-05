package pdef;

import org.junit.Test;
import pdef.descriptors.InterfaceDescriptor;
import pdef.descriptors.MethodDescriptor;
import pdef.test.interfaces.NextTestInterface;
import pdef.test.interfaces.TestInterface;

import java.util.List;

import static org.junit.Assert.*;
import static org.mockito.Mockito.RETURNS_DEEP_STUBS;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class InvocationTest {
	private final InterfaceDescriptor iface = TestInterface.DESCRIPTOR;
	private final MethodDescriptor indexMethod = iface.findMethod("indexMethod");
	private final MethodDescriptor interfaceMethod = iface.findMethod( "interfaceMethod");
	private final MethodDescriptor nextStringMethod = NextTestInterface.DESCRIPTOR
			.findMethod("stringMethod");

	@Test
	public void testIsRoot() throws Exception {
		Invocation root = Invocation.root();
		Invocation next = root.next(indexMethod, new Object[]{null, null});

		assertTrue(root.isRoot());
		assertFalse(next.isRoot());
	}

	@Test
	public void testGetArgs() throws Exception {
		Invocation invocation = Invocation.root().next(indexMethod, new Object[]{1, 2});
		assertArrayEquals(new Object[]{1, 2}, invocation.getArgs());
	}

	@Test
	public void testGetMethod() throws Exception {
		Invocation invocation = Invocation.root().next(indexMethod, new Object[]{1, 2});
		assertEquals(indexMethod, invocation.getMethod());
	}

	@Test
	public void testGetResult() throws Exception {
		Invocation invocation = Invocation.root().next(indexMethod, new Object[]{1, 2});
		assertEquals(indexMethod.getResult(), invocation.getResult());
	}

	@Test
	public void testGetExc() throws Exception {
		Invocation invocation = Invocation.root().next(indexMethod, new Object[]{1, 2});
		assertEquals(indexMethod.getExc(), invocation.getExc());
	}

	@Test
	public void testIsRemote() throws Exception {
		Invocation root = Invocation.root();
		Invocation indexInvocation = root.next(indexMethod, new Object[]{1, 2});
		Invocation interfaceInvocation = root.next(interfaceMethod, new Object[]{1, 2});

		assertFalse(root.isRemote());
		assertFalse(interfaceInvocation.isRemote());
		assertTrue(indexInvocation.isRemote());
	}

	@Test
	public void testToChain() throws Exception {
		List<Invocation> chain = Invocation.root()
				.next(interfaceMethod, new Object[]{1, 2})
				.next(nextStringMethod, new Object[]{"hello"})
				.toChain();

		assertEquals(2, chain.size());
	}

	@Test
	public void testInvoke() throws Exception {
		TestInterface iface = mock(TestInterface.class);
		when(iface.indexMethod(1, 2)).thenReturn(3);

		Invocation invocation = Invocation.root().next(indexMethod, new Object[]{1, 2});
		Object result = invocation.invoke(iface);
		assertEquals(3, result);
	}

	@Test
	public void testInvoke_chained() throws Exception {
		TestInterface iface = mock(TestInterface.class, RETURNS_DEEP_STUBS);
		when(iface.interfaceMethod(1, 2).stringMethod("hello")).thenReturn("good bye");

		Invocation invocation = Invocation.root()
				.next(interfaceMethod, new Object[]{1, 2})
				.next(nextStringMethod, new Object[]{"hello"});

		Object result = invocation.invoke(iface);
		assertEquals("good bye", result);
	}

	@Test
	public void testInvokeSingle() throws Exception {
		TestInterface iface = mock(TestInterface.class);
		when(iface.indexMethod(1, 2)).thenReturn(3);

		Invocation invocation = Invocation.root().next(indexMethod, new Object[]{1, 2});
		Object result = invocation.invokeSingle(iface);
		assertEquals(3, result);
	}
}