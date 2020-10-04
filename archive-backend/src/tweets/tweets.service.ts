import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Tweet, TweetDocument } from './schemas/tweet.schema';

@Injectable()
export class TweetsService {
  constructor(
    @InjectModel(Tweet.name) private tweetModel: Model<TweetDocument>,
  ) {}

  async create(tweetData): Promise<Tweet> {
    const createdTweet = new this.tweetModel(tweetData);
    return createdTweet.save();
  }

  async findAll(query): Promise<Tweet[]> {
    if (query.search) {
      return this.tweetModel.find({ $text: { $search: query.search } }).exec();
    }

    return this.tweetModel.find().exec();
  }
}
