/**
 * Offline build compatibility for Recharts 2.x.
 *
 * `@types/lodash` remains the declared development dependency and supplies the
 * complete lodash surface in normal installs. This intentionally models only
 * the single type Recharts imports while the package registry is unavailable.
 */
declare module "lodash" {
  type DebouncedFunction = (...args: never[]) => unknown;

  export interface DebouncedFunc<T extends DebouncedFunction> {
    (...args: Parameters<T>): ReturnType<T> | undefined;
    cancel(): void;
    flush(): ReturnType<T> | undefined;
  }
}
