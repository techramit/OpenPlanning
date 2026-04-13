import { createInterface } from 'readline';
import chalk from 'chalk';
import { UI_CONSTANTS } from '../config/Constants.js';

export class UIManager {
  constructor() {
    this.rl = null;
    this.initializeReadline();
  }

  initializeReadline() {
    this.rl = createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: true,
      completer: this.getAutoCompleter(),
    });

    this.rl.on('SIGINT', () => {
      this.handleSIGINT();
    });
  }

  getAutoCompleter() {
    return (line) => {
      const completions = this.getAvailableCommands();
      const hits = completions.filter((c) => c.startsWith(line));
      return [hits.length ? hits : completions, line];
    };
  }

  getAvailableCommands() {
    return ['exit', 'quit', 'help', 'clear'];
  }

  clearScreen() {
    console.clear();
  }

  renderWelcome() {
    console.log();
    console.log(chalk.bold(UI_CONSTANTS.WELCOME_TITLE));
    console.log(chalk.gray(UI_CONSTANTS.WELCOME_SUBTITLE));
    console.log();
    console.log(chalk.gray(UI_CONSTANTS.WELCOME_PROMPT));
    console.log();
  }

  renderGoodbye() {
    console.log();
    console.log(chalk.gray(UI_CONSTANTS.GOODBYE_MESSAGE));
  }

  renderError(error) {
    console.error();
    console.error(chalk.red('Error:'), error.message);
    console.error();
  }

  async prompt() {
    return new Promise((resolve) => {
      this.rl.question(chalk.blue('>'), (input) => {
        resolve(input);
      });
    });
  }

  renderUserMessage(message) {
    console.log();
    console.log(chalk.bold('You:'), message);
  }

  renderAssistantMessage(message) {
    console.log();
    console.log(chalk.bold('Assistant:'), message);
    console.log();
  }

  handleSIGINT() {
    console.log();
    this.rl.close();
    this.renderGoodbye();
    process.exit(0);
  }

  async pause() {
    return new Promise((resolve) => {
      setTimeout(resolve, UI_CONSTANTS.PAUSE_DURATION);
    });
  }

  close() {
    if (this.rl) {
      this.rl.close();
    }
  }
}
