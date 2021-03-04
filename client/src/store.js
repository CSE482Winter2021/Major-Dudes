import { createStore, applyMiddleware, compose } from 'redux';
import { createLogger } from 'redux-logger';
import thunk from 'redux-thunk';
import ExecutionEnvironment from 'fbjs/lib/ExecutionEnvironment';
import { composeWithDevTools } from 'redux-devtools-extension';

import reducers from './reducers';

// use thunk middleware for actions involving asynchronous API calls
const middlewares = [thunk];

// use redux logger, if possible
if (ExecutionEnvironment.canUseDOM) {
  middlewares.push(
    createLogger({
      level: 'info',
      duration: true,
      collapsed: true,
    }),
  );
}

// if we are in dev, use redux dev tools
const composeCustom =
  process.env.NODE_ENV === 'development' ? composeWithDevTools : compose;

export default (initialState) => {
  // check for logged-in user
  const persistedUser = localStorage.getItem('userId');
  const persistedState =
    persistedUser !== 'null'
      ? { ...initialState, user: { id: persistedUser, logging_in: false } }
      : initialState;

  const store = createStore(
    reducers,
    persistedState,
    composeCustom(applyMiddleware(...middlewares)),
  );

  // persist logged-in user
  store.subscribe(() => {
    localStorage.setItem('userId', store.getState().user.id);
  });
  return store;
};
