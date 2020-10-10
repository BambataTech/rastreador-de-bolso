import React from 'react';

export default (props) => {
  //   const [search] = useState('');
  return (
    <div className="userInput">
      <input type="text" onChange={props.changed} value={props.search} />
    </div>
  );
};
