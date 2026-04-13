export class SessionState {
  constructor(options = {}) {
    this.id = options.id || null;
    this.startTime = options.startTime || null;
    this.messages = options.messages || [];
    this.metadata = options.metadata || {};
    this.isActive = true;
  }

  addMessage(sender, content) {
    this.messages.push({
      sender,
      content,
      timestamp: new Date(),
    });
  }

  endSession() {
    this.isActive = false;
    this.endTime = new Date();
  }

  getMessageHistory() {
    return this.messages;
  }

  toJSON() {
    return {
      id: this.id,
      startTime: this.startTime,
      endTime: this.endTime,
      messages: this.messages,
      metadata: this.metadata,
      isActive: this.isActive,
    };
  }
}
