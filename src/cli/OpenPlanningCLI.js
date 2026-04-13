import { UIManager } from '../ui/UIManager.js';
import { Config } from '../config/Config.js';
import { SessionState } from '../types/SessionState.js';

export class OpenPlanningCLI {
  constructor() {
    this.config = new Config();
    this.ui = new UIManager();
    this.session = null;
  }

  async run() {
    try {
      this.session = new SessionState({
        id: this.generateSessionId(),
        startTime: new Date(),
      });

      await this.initializeCLI();
      await this.startREPL();
    } catch (error) {
      this.handleError(error);
    }
  }

  async initializeCLI() {
    this.ui.clearScreen();
    this.ui.renderWelcome();
  }

  async startREPL() {
    while (this.session.isActive) {
      try {
        const input = await this.ui.prompt();

        if (this.shouldExit(input)) {
          this.session.endSession();
          this.ui.close();
          this.ui.renderGoodbye();
          break;
        }

        await this.processInput(input);
      } catch (error) {
        this.ui.renderError(error);
      }
    }
  }

  async processInput(input) {
    this.session.addMessage('user', input);
    this.ui.renderUserMessage(input);

    const response = await this.generateResponse(input);
    this.session.addMessage('assistant', response);
    this.ui.renderAssistantMessage(response);
  }

  async generateResponse(input) {
    return `[Assistant](/mnt/d/Docs/SkyThink/OpenPlanning/src/config/Constants.js) received: "${input}"`;
  }

  shouldExit(input) {
    return this.config.exitCommands.includes(input.trim().toLowerCase());
  }

  async handleExit() {
    this.ui.renderGoodbye();
    await this.ui.pause();
  }

  handleError(error) {
    this.ui.renderError(error);
    process.exit(1);
  }

  generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
