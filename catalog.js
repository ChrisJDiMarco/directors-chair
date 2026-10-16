export const locations=[
{id:'diner',name:'Philadelphia diner',tag:'Intimacy · eyelines · reaction',description:'Warm practicals, green leather and blue-hour windows. A goodbye can begin in the space between two people.',color:'#b89a58'},
{id:'loft',name:'The loft apartment',tag:'Alliances · staging · reveal',description:'An intimate living room with a deep sofa, books and tall windows. Make the room reveal what a person cannot say.',color:'#af7f67'},
{id:'interview',name:'The interview room',tag:'Power · hard light · offscreen space',description:'A bare table, observation glass and an empty chair. Small framing choices change who holds the power.',color:'#8ca6a6'},
{id:'rooftop',name:'The rooftop terrace',tag:'Scale · silhouettes · ensemble',description:'A terrace above the city. Place a private decision against the scale of a skyline.',color:'#718caa'},
{id:'television',name:'The television studio',tag:'Master · singles · panel coverage',description:'A working interview floor with a desk, guest seating and scenic lighting. Direct a clear broadcast sequence.',color:'#72aaa7'}];
export const scenarios=[
['goodbye','diner','An Unspoken Goodbye',2,'Tell us who is leaving before anyone speaks.','Negative space and reaction coverage.','Record a wide, one restrained single, and a held reaction.'],
['listening','diner','Someone Is Listening',3,'Reveal a third person’s attention without an explanatory cut.','Foreground and background relationships.','Place the observer behind a lead; compare a shared frame with an isolated reaction.'],
['family','diner','The Family Table',6,'Make one quiet person readable in a busy social space.','Ensemble hierarchy and selective coverage.','Establish the room, then find the person who feels outside the group.'],
['confession','loft','The Confession',2,'Make the listener carry the scene.','Camera height and reaction timing.','Compare a balanced two-shot with an unequal composition.'],
['truth','loft','Three Versions of the Truth',3,'Make changing alliances legible.','Triangular blocking and screen direction.','Frame each pair, then include the excluded third person.'],
['surprise','loft','The Surprise',5,'Hide a reveal without losing the geography of the room.','Foreground masking and a group reaction.','Use furniture as a foreground layer, then reveal the whole group.'],
['question','interview','The Last Question',2,'Shift authority without moving the table.','Hard light, camera height and frame size.','Record the same person from eye level and a lower camera.'],
['witness','interview','The Witness',3,'Distinguish witness, questioner and observer.','Asymmetric blocking and reaction ownership.','Make a master and singles of the witness and observer.'],
['evidence','interview','Alone With the Evidence',1,'Make an empty chair matter.','Offscreen space and solitude.','Include the empty chair, then remove it from the frame and compare.'],
['dawn','rooftop','Before Dawn',2,'Make a decision feel larger than the conversation.','Skyline separation and scale.','Establish the city, then isolate one face against the skyline.'],
['deal','rooftop','The Deal',4,'Clarify who controls the meeting.','Opposing groups and a shared axis.','Arrange two sides, record a master, then coverage of each side.'],
['farewell','rooftop','The Farewell',8,'Build an ensemble frame with a clear emotional center.','Depth, overlap and selective isolation.','Keep all eight in the wide, then find one reaction without moving the cast.'],
['first-interview','television','The First Interview',2,'Make the host and guest feel connected.','Master, host single and guest single.','Save a master to A, host to B and guest to C. Record each setup.'],
['panel','television','The Panel',5,'Organize a host and four guests.','Balanced panel coverage and reactions.','Save the panel master, then make a useful single of each participant.'],
['breaking','television','Breaking Tonight',3,'Build an urgent but comprehensible broadcast sequence.','Anchor, correspondent and analyst coverage.','Assign three clear setups to A/B/C, then choose a deliberate cut order.']
].map(([id,sceneId,title,count,mission,concept,experiment])=>({id,sceneId,title,count,mission,concept,experiment}));
export const castNames=['Ella','James','Maya','Theo','Nora','Alex','Sam','Rowan'];
export function actorDefault(i,sceneId='diner'){
 const seating={diner:[[-.21,-.55,90],[1.69,-.55,-90],[-3.88,-1.4,90],[-1.89,-1.4,-90],[2.69,-1.4,90],[4.53,-1.4,-90]],loft:[[-1.65,-1.55,0],[1.55,-.5,-55],[-.35,-1.55,0]],interview:[[-1.5,-.6,90],[1.5,-.6,-90]],rooftop:[[-2.8,-1.2,25],[2.8,-1.2,-25]],television:[[-2,-.45,35],[1.2,-.7,-25],[2.45,-.7,-25],[3.7,-.7,-25],[.1,-.7,-25]]};
 const seats=seating[sceneId]||seating.diner,v=seats[i];return {id:'cast-'+(i+1),seatIndex:i,name:castNames[i],appearance:i%2,position:v?[v[0],sceneId==='loft'?.015:0,v[1]]:[(i-seats.length-(7-seats.length)/2)*1.1,sceneId==='loft'?.015:0,1.45],turn:v?v[2]:180,standing:!v};
}
export const scenarioById=id=>scenarios.find(s=>s.id===id)||scenarios[0];
