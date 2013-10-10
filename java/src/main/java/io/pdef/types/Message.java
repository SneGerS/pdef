package io.pdef.types;

import java.util.Map;

public interface Message {
	/** Returns a deep copy of this message. */
	Message copy();

	/** Returns this message type. */
	MessageType<? extends Message> type();
	
	/** Serializes this message to a map. */
	Map<String, Object> serializeToMap();

	/** Serializes this message to a JSON string without indentation. */
	String serializeToJson();

	/** Serializes this method to a JSON string with optional indentation. */
	String serializeToJson(boolean indent);
}