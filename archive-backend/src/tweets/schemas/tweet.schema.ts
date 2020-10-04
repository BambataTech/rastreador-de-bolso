import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

export type TweetDocument = Tweet & Document;

@Schema()
export class Tweet {
  @Prop()
  text: string;

  @Prop()
  retweet_count: number;

  @Prop()
  id_str: string;
}

export const TweetSchema = SchemaFactory.createForClass(Tweet);
