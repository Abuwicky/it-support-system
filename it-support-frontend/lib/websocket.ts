import { useEffect, useRef } from "react";

export function useTicketWebSocket(
  ticketId: number,
  onUpdate: (data: any) => void,
) {
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}/ticket/${ticketId}/?token=${token}`;

    socketRef.current = new WebSocket(wsUrl);

    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onUpdate(data);
    };

    return () => {
      socketRef.current?.close();
    };
  }, [ticketId]);
}
