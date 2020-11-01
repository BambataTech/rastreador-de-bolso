import axios from 'axios';
import React, { useState } from 'react';
import { useEffect } from 'react';
import Tweet from './Tweet';

export default ({ search }) => {
  const [tweets, setTweets] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get(
        `http://localhost:3000/tweets?search=${search}`
      );
      setTweets(result.data);
    };

    fetchData();
  }, [search]);

  return tweets.map((t) => <Tweet tweet={t}></Tweet>);
};
