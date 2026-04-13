export class Config {
  constructor(overrides = {}) {
    Object.assign(this, this.getDefaults(), overrides);
  }

  getDefaults() {
    return {
      exitCommands: ['exit', 'quit', 'q'],
      pauseDuration: 1000,
      debug: process.env.DEBUG === 'true',
    };
  }

  get(key) {
    return this[key];
  }

  set(key, value) {
    this[key] = value;
  }
}
