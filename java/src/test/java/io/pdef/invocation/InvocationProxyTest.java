package io.pdef.invocation;

import com.google.common.base.Function;
import io.pdef.test.interfaces.TestException;
import io.pdef.test.interfaces.TestInterface;
import io.pdef.types.InterfaceMethod;
import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;
import static org.mockito.Matchers.any;
import org.mockito.Mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import static org.mockito.MockitoAnnotations.initMocks;

import java.util.List;

public class InvocationProxyTest {
	@Mock Function<Invocation, InvocationResult> handler;

	@Before
	public void setUp() throws Exception {
		initMocks(this);
	}

	@Test
	public void testInvoke_handle() throws Throwable {
		TestInterface iface = createProxy();
		when(handler.apply(any(Invocation.class))).thenReturn(InvocationResult.ok(3));

		Object result = iface.indexMethod(1, 2);
		assertEquals(3, result);
	}

	@Test(expected = TestException.class)
	public void testInvoke_handleExc() throws Exception {
		TestInterface iface = createProxy();
		when(handler.apply(any(Invocation.class)))
				.thenReturn(InvocationResult.exc(new TestException()));

		iface.excMethod();
	}

	@Test
	public void testInvoke_capture() throws Exception {
		TestInterface iface = createProxy();
		ArgumentCaptor<Invocation> captor = ArgumentCaptor.forClass(Invocation.class);
		when(handler.apply(any(Invocation.class))).thenReturn(InvocationResult.ok(null));

		iface.indexMethod(1, 2);
		verify(handler).apply(captor.capture());

		Invocation invocation = captor.getValue();
		InterfaceMethod method = getIndexMethod();
		assertEquals(method, invocation.getMethod());
		assertArrayEquals(new Object[]{1, 2}, invocation.getArgs());
	}

	@Test
	public void testInvoke_captureChain() throws Exception {
		TestInterface iface = createProxy();
		ArgumentCaptor<Invocation> captor = ArgumentCaptor.forClass(Invocation.class);
		when(handler.apply(any(Invocation.class))).thenReturn(InvocationResult.ok(null));

		iface.interfaceMethod(1, 2).stringMethod("hello");
		verify(handler).apply(captor.capture());

		List<Invocation> chain = captor.getValue().toChain();
		assertEquals(2, chain.size());

		Invocation invocation0 = chain.get(0);
		Invocation invocation1 = chain.get(1);
		assertArrayEquals(new Object[]{1, 2}, invocation0.getArgs());
		assertArrayEquals(new Object[]{"hello"}, invocation1.getArgs());
	}

	private TestInterface createProxy() {
		return InvocationProxy.create(TestInterface.class, TestInterface.TYPE, handler);
	}

	private InterfaceMethod getIndexMethod() {
		return TestInterface.TYPE.findMethod("indexMethod");
	}
}
