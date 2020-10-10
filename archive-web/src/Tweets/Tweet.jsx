import React from 'react';
import './Tweet.css';

export default (props) => {
  return (
    <a
      className="twitter-link"
      href={`https://twitter.com/jairbolsonaro/status/${props.tweet.id}`}
    >
      <blockquote
        className="twitter-tweet"
        data-conversation="none"
        data-theme="light"
      >
        <p lang="pt" dir="ltr">
          {props.tweet.full_text}
        </p>
        &mdash; Jair M. Bolsonaro (@jairbolsonaro)
      </blockquote>
    </a>
  );
};
